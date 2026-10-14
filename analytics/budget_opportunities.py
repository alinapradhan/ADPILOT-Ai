import pandas as pd

from schemas.responses import BudgetOpportunity


class BudgetOpportunityAnalyzer:
    def analyze(self, current_frame: pd.DataFrame, target_roas: float) -> list[BudgetOpportunity]:
        opportunities: list[BudgetOpportunity] = []
        for (campaign_id, campaign_name), group in current_frame.groupby(
            ["campaign_id", "campaign_name"], dropna=False
        ):
            spend = float(group["spend"].sum(min_count=1) or 0)
            revenue = float(group["revenue"].sum(min_count=1) or 0)
            conversions = float(group["conversions"].sum(min_count=1) or 0)
            roas = (revenue / spend) if spend else None

            if roas is None:
                opportunities.append(
                    BudgetOpportunity(
                        campaign_id=str(campaign_id),
                        campaign_name=str(campaign_name),
                        recommendation="Investigate first",
                        reason="Spend is zero or missing; cannot estimate efficiency",
                        estimated_outcome="Insufficient data for deterministic projection",
                        uncertainty="High",
                    )
                )
            elif roas >= target_roas:
                opportunities.append(
                    BudgetOpportunity(
                        campaign_id=str(campaign_id),
                        campaign_name=str(campaign_name),
                        recommendation="Consider scaling",
                        reason=f"ROAS {roas:.2f} is above target {target_roas:.2f}",
                        estimated_outcome="If performance holds, additional spend may increase revenue proportionally",
                        uncertainty="Medium",
                    )
                )
            else:
                opportunities.append(
                    BudgetOpportunity(
                        campaign_id=str(campaign_id),
                        campaign_name=str(campaign_name),
                        recommendation="Prioritize efficiency review",
                        reason=f"ROAS {roas:.2f} is below target {target_roas:.2f}",
                        estimated_outcome=f"At current efficiency, each extra 100 spend is expected to return {roas * 100:.2f} revenue",
                        uncertainty="Medium",
                    )
                )

            if conversions == 0:
                opportunities[-1].uncertainty = "High"
                opportunities[-1].reason += "; no observed conversions in period"
        return opportunities
