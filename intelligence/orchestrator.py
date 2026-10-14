from analytics.anomaly_detector import AnomalyDetector
from analytics.baseline_analyzer import BaselineAnalyzer
from analytics.metrics_engine import MetricsEngine
from investigations.planner import InvestigationPlanner
from intelligence.evidence_builder import EvidenceBuilder
from llm.interpreter import LLMInterpreter
from schemas.requests import InvestigationRequest
from schemas.responses import AnalysisPreviewResponse, InvestigationResponse
from services.run_store import AnalysisRunStore
from validation.claim_validator import ClaimValidator


class IntelligenceOrchestrator:
    def __init__(self, run_store: AnalysisRunStore) -> None:
        self.metrics = MetricsEngine()
        self.baseline = BaselineAnalyzer()
        self.anomalies = AnomalyDetector()
        self.planner = InvestigationPlanner()
        self.evidence = EvidenceBuilder()
        self.interpreter = LLMInterpreter()
        self.validator = ClaimValidator()
        self.run_store = run_store

    def build_preview(
        self,
        *,
        run_id: str,
        current_metrics: dict[str, float | None],
        baseline_metrics: dict[str, float | None],
        missing_data: list[str],
    ) -> AnalysisPreviewResponse:
        comparisons = self.baseline.compare(
            current_metrics,
            baseline_metrics,
            ["spend", "clicks", "conversions", "cpa", "ctr", "roas"],
        )
        self.run_store.attach_comparisons(run_id, comparisons)
        return AnalysisPreviewResponse(run_id=run_id, metrics=comparisons, missing_data=missing_data)

    def investigate(
        self,
        *,
        request: InvestigationRequest,
        run_id: str,
        current_metrics: dict[str, float | None],
        baseline_metrics: dict[str, float | None],
        source: str,
    ) -> InvestigationResponse:
        plan = self.planner.build_plan(request)
        comparisons = self.baseline.compare(
            current_metrics,
            baseline_metrics,
            ["spend", "clicks", "conversions", "cpa", "ctr", "roas"],
        )
        anomalies = self.anomalies.detect(comparisons)
        findings = self.evidence.build_findings(
            anomalies,
            reporting_period=f"{request.window.current_start} to {request.window.current_end}",
            source=source,
        )
        summary = self.interpreter.interpret_findings(findings, request.question)
        issues = self.validator.validate(findings)
        self.run_store.attach_findings(run_id, findings)
        self.run_store.attach_narrative(run_id, summary)
        self.run_store.attach_validation_issues(run_id, issues)

        return InvestigationResponse(
            run_id=run_id,
            question=request.question,
            plan=plan,
            findings=findings,
        )
