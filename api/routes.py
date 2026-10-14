from collections import Counter

from fastapi import APIRouter, Depends, HTTPException

from analytics.budget_opportunities import BudgetOpportunityAnalyzer
from analytics.campaign_health import CampaignHealthScorer
from analytics.normalizer import DataNormalizer
from core.config import settings
from intelligence.orchestrator import IntelligenceOrchestrator
from schemas.common import Finding
from schemas.requests import (
    AnalysisPreviewRequest,
    AssistantAskRequest,
    BudgetOpportunityRequest,
    CampaignHealthRequest,
    InvestigationRequest,
    ValidateRunRequest,
)
from schemas.responses import (
    AnalysisPreviewResponse,
    AnalysisRunDetail,
    AnalysisRunSummary,
    AssistantResponse,
    BudgetOpportunityResponse,
    CampaignHealthResponse,
    ConnectorFieldsResponse,
    ConnectorSummary,
    HealthResponse,
    InvestigationResponse,
    ValidationResponse,
)
from services.auth import authorize_scope, get_current_user_id
from services.provider_registry import ProviderRegistry
from services.run_store import AnalysisRunStore
from validation.claim_validator import ClaimValidator

from .dependencies import get_provider_registry, get_run_store

router = APIRouter()
normalizer = DataNormalizer()
health_scorer = CampaignHealthScorer()
budget_analyzer = BudgetOpportunityAnalyzer()
validator = ClaimValidator()


async def _load_frames(
    request_scope,
    request_window,
    registry: ProviderRegistry,
):
    provider = registry.for_connector(request_scope.connector)
    fields = await provider.get_fields(request_scope.connector)
    current_records = await provider.fetch_records(
        connector=request_scope.connector,
        account_id=request_scope.account_id,
        start_date=request_window.current_start,
        end_date=request_window.current_end,
        fields=fields,
    )
    baseline_records = await provider.fetch_records(
        connector=request_scope.connector,
        account_id=request_scope.account_id,
        start_date=request_window.baseline_start,
        end_date=request_window.baseline_end,
        fields=fields,
    )
    return normalizer.to_frame(current_records), normalizer.to_frame(baseline_records)


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


@router.get("/connectors", response_model=list[ConnectorSummary])
async def connectors(registry: ProviderRegistry = Depends(get_provider_registry)) -> list[ConnectorSummary]:
    connector_list = await registry.list_connectors()
    return [ConnectorSummary(**item) for item in connector_list]


@router.get("/connectors/{connector}/fields", response_model=ConnectorFieldsResponse)
async def connector_fields(
    connector: str,
    registry: ProviderRegistry = Depends(get_provider_registry),
) -> ConnectorFieldsResponse:
    provider = registry.for_connector(connector)
    fields = await provider.get_fields(connector)
    return ConnectorFieldsResponse(connector=connector, fields=fields)


@router.post("/analysis/preview", response_model=AnalysisPreviewResponse)
async def analysis_preview(
    request: AnalysisPreviewRequest,
    user_id: str = Depends(get_current_user_id),
    registry: ProviderRegistry = Depends(get_provider_registry),
    store: AnalysisRunStore = Depends(get_run_store),
) -> AnalysisPreviewResponse:
    authorize_scope(user_id=user_id, client_id=request.scope.client_id, account_id=request.scope.account_id)
    current_frame, baseline_frame = await _load_frames(request.scope, request.window, registry)
    orchestrator = IntelligenceOrchestrator(store)
    current_metrics = orchestrator.metrics.aggregate(current_frame)
    baseline_metrics = orchestrator.metrics.aggregate(baseline_frame)
    missing = [
        metric for metric, value in current_metrics.items() if value is None
    ]
    run_id = store.create_run(
        analysis_type="preview",
        client_id=request.scope.client_id,
        account_id=request.scope.account_id,
        input_payload=request.model_dump(mode="json"),
    )
    return orchestrator.build_preview(
        run_id=run_id,
        current_metrics=current_metrics,
        baseline_metrics=baseline_metrics,
        missing_data=missing,
    )


@router.post("/analysis/campaign-health", response_model=CampaignHealthResponse)
async def campaign_health(
    request: CampaignHealthRequest,
    user_id: str = Depends(get_current_user_id),
    registry: ProviderRegistry = Depends(get_provider_registry),
    store: AnalysisRunStore = Depends(get_run_store),
) -> CampaignHealthResponse:
    authorize_scope(user_id=user_id, client_id=request.scope.client_id, account_id=request.scope.account_id)
    current_frame, baseline_frame = await _load_frames(request.scope, request.window, registry)
    run_id = store.create_run(
        analysis_type="campaign-health",
        client_id=request.scope.client_id,
        account_id=request.scope.account_id,
        input_payload=request.model_dump(mode="json"),
    )
    campaigns = health_scorer.score(
        current_frame,
        baseline_frame,
        target_cpa=request.target_cpa,
        target_roas=request.target_roas,
    )
    return CampaignHealthResponse(
        run_id=run_id,
        method_summary="Weighted score with configurable target CPA/ROAS, trends, and completeness checks.",
        campaigns=campaigns,
    )


@router.post("/analysis/investigate", response_model=InvestigationResponse)
async def investigate(
    request: InvestigationRequest,
    user_id: str = Depends(get_current_user_id),
    registry: ProviderRegistry = Depends(get_provider_registry),
    store: AnalysisRunStore = Depends(get_run_store),
) -> InvestigationResponse:
    authorize_scope(user_id=user_id, client_id=request.scope.client_id, account_id=request.scope.account_id)
    current_frame, baseline_frame = await _load_frames(request.scope, request.window, registry)
    run_id = store.create_run(
        analysis_type="investigate",
        client_id=request.scope.client_id,
        account_id=request.scope.account_id,
        input_payload=request.model_dump(mode="json"),
    )
    orchestrator = IntelligenceOrchestrator(store)
    return orchestrator.investigate(
        request=request,
        run_id=run_id,
        current_metrics=orchestrator.metrics.aggregate(current_frame),
        baseline_metrics=orchestrator.metrics.aggregate(baseline_frame),
        source=request.scope.connector,
    )


@router.post("/analysis/budget-opportunities", response_model=BudgetOpportunityResponse)
async def budget_opportunities(
    request: BudgetOpportunityRequest,
    user_id: str = Depends(get_current_user_id),
    registry: ProviderRegistry = Depends(get_provider_registry),
    store: AnalysisRunStore = Depends(get_run_store),
) -> BudgetOpportunityResponse:
    authorize_scope(user_id=user_id, client_id=request.scope.client_id, account_id=request.scope.account_id)
    current_frame, baseline_frame = await _load_frames(request.scope, request.window, registry)
    del baseline_frame
    run_id = store.create_run(
        analysis_type="budget-opportunities",
        client_id=request.scope.client_id,
        account_id=request.scope.account_id,
        input_payload=request.model_dump(mode="json"),
    )
    opportunities = budget_analyzer.analyze(current_frame, request.target_roas)
    return BudgetOpportunityResponse(run_id=run_id, opportunities=opportunities)


@router.post("/assistant/ask", response_model=AssistantResponse)
async def assistant_ask(
    request: AssistantAskRequest,
    user_id: str = Depends(get_current_user_id),
    store: AnalysisRunStore = Depends(get_run_store),
) -> AssistantResponse:
    authorize_scope(user_id=user_id, client_id=request.scope.client_id, account_id=request.scope.account_id)
    runs = [run for run in store.list_runs() if run.client_id == request.scope.client_id and run.account_id == request.scope.account_id]
    if not runs:
        run_id = store.create_run(
            analysis_type="assistant",
            client_id=request.scope.client_id,
            account_id=request.scope.account_id,
            input_payload=request.model_dump(mode="json"),
        )
        return AssistantResponse(
            run_id=run_id,
            answer="No prior analysis context exists for this scope.",
            evidence_summary=[],
            unavailable_reason="Run preview or investigation first.",
        )

    latest = runs[0]
    findings = store.get_findings(latest.run_id)
    evidence = [f"{f.metric}: current={f.current_value}, baseline={f.comparison_value}" for f in findings]
    run_id = store.create_run(
        analysis_type="assistant",
        client_id=request.scope.client_id,
        account_id=request.scope.account_id,
        input_payload=request.model_dump(mode="json"),
    )
    if not findings:
        answer = "I do not have sufficient validated findings yet; please run an investigation for evidence-backed insights."
    else:
        severity_counts = Counter(f.severity for f in findings)
        answer = (
            f"Top priorities: {severity_counts.get('high', 0)} high, {severity_counts.get('medium', 0)} medium findings. "
            "Review high-severity findings first and validate missing segments before deciding budget shifts."
        )
    return AssistantResponse(run_id=run_id, answer=answer, evidence_summary=evidence)


@router.get("/analysis/runs", response_model=list[AnalysisRunSummary])
async def list_runs(store: AnalysisRunStore = Depends(get_run_store)) -> list[AnalysisRunSummary]:
    return store.list_runs()


@router.get("/analysis/runs/{run_id}", response_model=AnalysisRunDetail)
async def get_run(run_id: str, store: AnalysisRunStore = Depends(get_run_store)) -> AnalysisRunDetail:
    try:
        return store.get_run(run_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Run not found") from exc


@router.get("/analysis/runs/{run_id}/findings", response_model=list[Finding])
async def get_run_findings(
    run_id: str,
    store: AnalysisRunStore = Depends(get_run_store),
) -> list[Finding]:
    return store.get_findings(run_id)


@router.post("/analysis/runs/{run_id}/validate", response_model=ValidationResponse)
async def validate_run(
    run_id: str,
    request: ValidateRunRequest,
    store: AnalysisRunStore = Depends(get_run_store),
) -> ValidationResponse:
    if run_id != request.run_id:
        raise HTTPException(status_code=400, detail="run_id in path and payload must match")
    findings = store.get_findings(run_id)
    issues = validator.validate(findings)
    return ValidationResponse(run_id=run_id, valid=not issues, issues=issues)
