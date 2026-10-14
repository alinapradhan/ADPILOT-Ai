from pprint import pprint

from analytics.metrics_engine import MetricsEngine
from analytics.normalizer import DataNormalizer
from data.synthetic_provider_data import SYNTHETIC_RECORDS
from intelligence.orchestrator import IntelligenceOrchestrator
from schemas.common import CampaignRecord
from schemas.requests import AnalysisScope, AnalysisWindow, InvestigationRequest
from services.run_store import AnalysisRunStore


if __name__ == "__main__":
    normalizer = DataNormalizer()
    metrics = MetricsEngine()

    current = [CampaignRecord(**row) for row in SYNTHETIC_RECORDS if row["date"].month == 10]
    baseline = [CampaignRecord(**row) for row in SYNTHETIC_RECORDS if row["date"].month == 9]

    current_frame = normalizer.to_frame(current)
    baseline_frame = normalizer.to_frame(baseline)

    run_store = AnalysisRunStore()
    orchestrator = IntelligenceOrchestrator(run_store)
    run_id = run_store.create_run(
        analysis_type="investigate",
        client_id="client-a",
        account_id="acct-1",
        input_payload={},
    )
    request = InvestigationRequest(
        scope=AnalysisScope(client_id="client-a", account_id="acct-1", connector="mock_ads"),
        window=AnalysisWindow(
            current_start="2026-10-01",
            current_end="2026-10-31",
            baseline_start="2026-09-01",
            baseline_end="2026-09-30",
        ),
        question="Why did CPA increase this month?",
    )

    response = orchestrator.investigate(
        request=request,
        run_id=run_id,
        current_metrics=metrics.aggregate(current_frame),
        baseline_metrics=metrics.aggregate(baseline_frame),
        source="mock_ads",
    )

    print("=== Investigation Findings ===")
    pprint(response.model_dump())
    print("\nAdditional data needed for causal proof: creative changes, auction pressure, audience overlap, tracking checks.")
