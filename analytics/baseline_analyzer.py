from schemas.responses import ComparisonMetric


class BaselineAnalyzer:
    def compare(
        self,
        current: dict[str, float | None],
        baseline: dict[str, float | None],
        metrics: list[str],
    ) -> list[ComparisonMetric]:
        comparisons: list[ComparisonMetric] = []
        for metric in metrics:
            current_value = current.get(metric)
            baseline_value = baseline.get(metric)
            if baseline_value in (None, 0) or current_value is None:
                change_pct = None
            else:
                change_pct = ((current_value - baseline_value) / baseline_value) * 100
            comparisons.append(
                ComparisonMetric(
                    metric=metric,
                    current=current_value,
                    baseline=baseline_value,
                    change_pct=change_pct,
                )
            )
        return comparisons
