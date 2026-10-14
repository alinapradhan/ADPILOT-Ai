from schemas.responses import ComparisonMetric


class AnomalyDetector:
    def __init__(self, threshold_pct: float = 20.0) -> None:
        self.threshold_pct = threshold_pct

    def detect(self, comparisons: list[ComparisonMetric]) -> list[ComparisonMetric]:
        return [
            comparison
            for comparison in comparisons
            if comparison.change_pct is not None and abs(comparison.change_pct) >= self.threshold_pct
        ]
