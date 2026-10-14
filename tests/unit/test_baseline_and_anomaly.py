from analytics.anomaly_detector import AnomalyDetector
from analytics.baseline_analyzer import BaselineAnalyzer


def test_baseline_comparison_and_anomaly_detection() -> None:
    current = {"spend": 150.0, "conversions": 5.0}
    baseline = {"spend": 100.0, "conversions": 8.0}
    analyzer = BaselineAnalyzer()
    comparisons = analyzer.compare(current, baseline, ["spend", "conversions"])

    spend = next(item for item in comparisons if item.metric == "spend")
    assert round(spend.change_pct or 0, 2) == 50.0

    anomalies = AnomalyDetector(threshold_pct=20).detect(comparisons)
    assert len(anomalies) == 2
