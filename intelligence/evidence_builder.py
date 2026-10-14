from schemas.common import Finding, Severity
from schemas.responses import ComparisonMetric


class EvidenceBuilder:
    def build_findings(
        self,
        comparisons: list[ComparisonMetric],
        reporting_period: str,
        source: str,
    ) -> list[Finding]:
        findings: list[Finding] = []
        for comparison in comparisons:
            if comparison.change_pct is None:
                continue
            severity = (
                Severity.high
                if abs(comparison.change_pct) >= 40
                else Severity.medium
                if abs(comparison.change_pct) >= 20
                else Severity.low
            )
            direction = "increased" if comparison.change_pct > 0 else "decreased"
            finding = Finding(
                finding_id=f"fnd-{comparison.metric}",
                title=f"{comparison.metric.upper()} {direction}",
                description=f"{comparison.metric} changed by {comparison.change_pct:.2f}% versus baseline",
                fact=f"Observed {comparison.metric} {direction} relative to baseline",
                hypothesis="Potential driver requires drill-down by campaign, audience, and placement",
                metric=comparison.metric,
                current_value=comparison.current,
                comparison_value=comparison.baseline,
                delta=(comparison.current - comparison.baseline) if comparison.current is not None and comparison.baseline is not None else None,
                calculation="(current - baseline) / baseline * 100",
                evidence_source=source,
                reporting_period=reporting_period,
                severity=severity,
                recommended_next_step="Review campaign-level segments and conversion quality for this metric",
            )
            findings.append(finding)
        return findings
