import pandas as pd

from analytics.metrics_engine import MetricsEngine


def test_metrics_engine_handles_zero_denominator() -> None:
    frame = pd.DataFrame(
        [
            {
                "spend": 100.0,
                "clicks": 0.0,
                "conversions": 0.0,
                "impressions": 0.0,
                "revenue": 0.0,
            }
        ]
    )
    metrics = MetricsEngine().aggregate(frame)
    assert metrics["cpa"] is None
    assert metrics["ctr"] is None
    assert metrics["cpc"] is None



def test_metrics_engine_calculates_roas() -> None:
    frame = pd.DataFrame(
        [
            {
                "spend": 200.0,
                "clicks": 100.0,
                "conversions": 8.0,
                "impressions": 1000.0,
                "revenue": 600.0,
            }
        ]
    )
    metrics = MetricsEngine().aggregate(frame)
    assert metrics["roas"] == 3.0
    assert metrics["cpa"] == 25.0
