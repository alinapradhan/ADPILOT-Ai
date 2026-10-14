from datetime import datetime

from pydantic import BaseModel

from schemas.common import Finding, HealthStatus


class HealthResponse(BaseModel):
    status: str
    service: str


class ConnectorSummary(BaseModel):
    connector: str
    description: str


class ConnectorFieldsResponse(BaseModel):
    connector: str
    fields: list[str]


class ComparisonMetric(BaseModel):
    metric: str
    current: float | None
    baseline: float | None
    change_pct: float | None


class AnalysisPreviewResponse(BaseModel):
    run_id: str
    metrics: list[ComparisonMetric]
    missing_data: list[str]


class CampaignHealthItem(BaseModel):
    campaign_id: str
    campaign_name: str
    status: HealthStatus
    spend_efficiency_score: float
    conversion_score: float
    trend_score: float
    data_completeness_score: float
    key_contributors: list[str]
    limitations: list[str]
    suggested_investigation_steps: list[str]


class CampaignHealthResponse(BaseModel):
    run_id: str
    method_summary: str
    campaigns: list[CampaignHealthItem]


class InvestigationResponse(BaseModel):
    run_id: str
    question: str
    plan: list[str]
    findings: list[Finding]


class BudgetOpportunity(BaseModel):
    campaign_id: str
    campaign_name: str
    recommendation: str
    reason: str
    estimated_outcome: str
    uncertainty: str


class BudgetOpportunityResponse(BaseModel):
    run_id: str
    opportunities: list[BudgetOpportunity]


class AssistantResponse(BaseModel):
    run_id: str
    answer: str
    evidence_summary: list[str]
    unavailable_reason: str | None = None


class AnalysisRunSummary(BaseModel):
    run_id: str
    analysis_type: str
    client_id: str
    account_id: str
    created_at: datetime


class AnalysisRunDetail(BaseModel):
    run_id: str
    analysis_type: str
    client_id: str
    account_id: str
    created_at: datetime
    input_payload: dict
    findings_count: int


class ValidationResponse(BaseModel):
    run_id: str
    valid: bool
    issues: list[str]
