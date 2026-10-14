import pandas as pd

from schemas.common import HealthStatus
from schemas.responses import CampaignHealthItem


class CampaignHealthScorer:
    def score(
        self,
        current_frame: pd.DataFrame,
        baseline_frame: pd.DataFrame,
        *,
        target_cpa: float,
        target_roas: float,
    ) -> list[CampaignHealthItem]:
        items: list[CampaignHealthItem] = []
        grouped_current = current_frame.groupby(["campaign_id", "campaign_name"], dropna=False)
        grouped_baseline = baseline_frame.groupby(["campaign_id", "campaign_name"], dropna=False)

        for (campaign_id, campaign_name), current_group in grouped_current:
            baseline_group = grouped_baseline.get_group((campaign_id, campaign_name)) if (campaign_id, campaign_name) in grouped_baseline.groups else pd.DataFrame(columns=current_group.columns)
            spend = current_group["spend"].sum(min_count=1)
            conversions = current_group["conversions"].sum(min_count=1)
            revenue = current_group["revenue"].sum(min_count=1)
            baseline_spend = baseline_group["spend"].sum(min_count=1)
            baseline_conversions = baseline_group["conversions"].sum(min_count=1)

            cpa = None if conversions in (None, 0) or pd.isna(conversions) else float(spend / conversions)
            roas = None if spend in (None, 0) or pd.isna(spend) else float(revenue / spend)
            spend_delta = None
            if baseline_spend not in (None, 0) and not pd.isna(baseline_spend):
                spend_delta = float((spend - baseline_spend) / baseline_spend * 100)

            conversion_delta = None
            if baseline_conversions not in (None, 0) and not pd.isna(baseline_conversions):
                conversion_delta = float((conversions - baseline_conversions) / baseline_conversions * 100)

            spend_efficiency_score = max(0.0, min(100.0, (target_cpa / cpa) * 100)) if cpa else 0.0
            conversion_score = max(0.0, min(100.0, (roas / target_roas) * 100)) if roas else 0.0
            trend_score = 50.0
            if spend_delta is not None and conversion_delta is not None:
                trend_score = max(0.0, min(100.0, 50.0 + conversion_delta - spend_delta))
            completeness = current_group[["spend", "clicks", "conversions", "impressions", "revenue"]].notna().mean().mean() * 100

            composite = (spend_efficiency_score * 0.35) + (conversion_score * 0.35) + (trend_score * 0.2) + (completeness * 0.1)
            if composite >= 70:
                status = HealthStatus.healthy
            elif composite >= 45:
                status = HealthStatus.watch
            else:
                status = HealthStatus.critical

            limitations = []
            if current_group["conversions"].isna().any():
                limitations.append("Missing conversion values reduce CPA confidence")
            if current_group["currency"].nunique() > 1:
                limitations.append("Multiple currencies in one campaign are not directly comparable")

            items.append(
                CampaignHealthItem(
                    campaign_id=str(campaign_id),
                    campaign_name=str(campaign_name),
                    status=status,
                    spend_efficiency_score=round(spend_efficiency_score, 2),
                    conversion_score=round(conversion_score, 2),
                    trend_score=round(trend_score, 2),
                    data_completeness_score=round(completeness, 2),
                    key_contributors=[
                        "CPA versus target",
                        "ROAS versus target",
                        "Spend and conversion trend",
                    ],
                    limitations=limitations,
                    suggested_investigation_steps=[
                        "Review placement/device level efficiency",
                        "Validate conversion tracking integrity",
                    ],
                )
            )
        return items
