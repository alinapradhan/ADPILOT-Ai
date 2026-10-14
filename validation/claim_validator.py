from schemas.common import Finding


class ClaimValidator:
    def validate(self, findings: list[Finding]) -> list[str]:
        issues: list[str] = []
        for finding in findings:
            if finding.current_value is None or finding.comparison_value is None:
                issues.append(
                    f"{finding.finding_id}: Missing numerical evidence for current or comparison value"
                )
            if finding.calculation.strip() == "":
                issues.append(f"{finding.finding_id}: Calculation formula missing")
        return issues
