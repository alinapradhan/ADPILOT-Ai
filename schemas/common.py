from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class HealthStatus(str, Enum):
    healthy = "healthy"
    watch = "watch"
    critical = "critical"


class ReportingWindow(BaseModel):
    start_date: date
    end_date: date


class ProviderMetadata(BaseModel):
    connector: str
    account_id: str
    reporting_window: ReportingWindow
    source_timezone: str = "UTC"


class CampaignRecord(BaseModel):
    campaign_id: str
    campaign_name: str
    date: date
    currency: str = "USD"
    spend: float | None = None
    clicks: float | None = None
    conversions: float | None = None
    impressions: float | None = None
    revenue: float | None = None


class Finding(BaseModel):
    finding_id: str
    title: str
    description: str
    fact: str
    hypothesis: str | None = None
    metric: str
    current_value: float | None = None
    comparison_value: float | None = None
    delta: float | None = None
    calculation: str
    evidence_source: str
    reporting_period: str
    severity: Severity
    recommended_next_step: str
    confidence_limitations: str = Field(
        default="Limited to available connector metrics and configured dimensions."
    )
