from schemas.common import Finding, Severity
from validation.claim_validator import ClaimValidator


def test_claim_validator_flags_missing_values() -> None:
    finding = Finding(
        finding_id="f-1",
        title="CPA increased",
        description="desc",
        fact="fact",
        metric="cpa",
        current_value=None,
        comparison_value=10.0,
        delta=None,
        calculation="(current-baseline)/baseline",
        evidence_source="mock",
        reporting_period="period",
        severity=Severity.high,
        recommended_next_step="step",
    )
    issues = ClaimValidator().validate([finding])
    assert issues
