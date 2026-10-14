from schemas.requests import InvestigationRequest


class InvestigationPlanner:
    def build_plan(self, request: InvestigationRequest) -> list[str]:
        return [
            "Confirm business question and comparison period",
            "Retrieve only required metrics and dimensions from provider",
            "Compute KPI deltas, anomalies, and campaign concentration",
            "Separate observed facts from causal hypotheses",
            "Generate recommendations ranked by potential impact",
            "List missing data needed to validate hypotheses",
        ]
