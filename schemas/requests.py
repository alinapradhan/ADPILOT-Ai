from datetime import date

from pydantic import BaseModel, Field


class AnalysisScope(BaseModel):
    client_id: str
    account_id: str
    connector: str = "mock_ads"


class AnalysisWindow(BaseModel):
    current_start: date
    current_end: date
    baseline_start: date
    baseline_end: date


class CampaignHealthRequest(BaseModel):
    scope: AnalysisScope
    window: AnalysisWindow
    target_cpa: float = Field(default=40.0, gt=0)
    target_roas: float = Field(default=2.5, gt=0)


class AnalysisPreviewRequest(BaseModel):
    scope: AnalysisScope
    window: AnalysisWindow


class InvestigationRequest(BaseModel):
    scope: AnalysisScope
    window: AnalysisWindow
    question: str


class BudgetOpportunityRequest(BaseModel):
    scope: AnalysisScope
    window: AnalysisWindow
    target_roas: float = Field(default=2.5, gt=0)


class AssistantAskRequest(BaseModel):
    scope: AnalysisScope
    question: str


class ValidateRunRequest(BaseModel):
    run_id: str
