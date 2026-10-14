from collections import defaultdict
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4

from schemas.common import Finding
from schemas.responses import AnalysisRunDetail, AnalysisRunSummary, ComparisonMetric


@dataclass
class RunRecord:
    run_id: str
    analysis_type: str
    client_id: str
    account_id: str
    created_at: datetime
    input_payload: dict
    comparisons: list[ComparisonMetric] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    narrative: str | None = None
    validation_issues: list[str] = field(default_factory=list)


class AnalysisRunStore:
    def __init__(self) -> None:
        self._runs: dict[str, RunRecord] = {}
        self._findings_by_run: defaultdict[str, list[Finding]] = defaultdict(list)

    def create_run(self, *, analysis_type: str, client_id: str, account_id: str, input_payload: dict) -> str:
        run_id = str(uuid4())
        self._runs[run_id] = RunRecord(
            run_id=run_id,
            analysis_type=analysis_type,
            client_id=client_id,
            account_id=account_id,
            created_at=datetime.now(UTC),
            input_payload=input_payload,
        )
        return run_id

    def attach_findings(self, run_id: str, findings: list[Finding]) -> None:
        run = self._runs[run_id]
        run.findings = findings
        self._findings_by_run[run_id] = findings

    def attach_comparisons(self, run_id: str, comparisons: list[ComparisonMetric]) -> None:
        self._runs[run_id].comparisons = comparisons

    def attach_narrative(self, run_id: str, narrative: str) -> None:
        self._runs[run_id].narrative = narrative

    def attach_validation_issues(self, run_id: str, issues: list[str]) -> None:
        self._runs[run_id].validation_issues = issues

    def list_runs(self) -> list[AnalysisRunSummary]:
        return [
            AnalysisRunSummary(
                run_id=run.run_id,
                analysis_type=run.analysis_type,
                client_id=run.client_id,
                account_id=run.account_id,
                created_at=run.created_at,
            )
            for run in sorted(self._runs.values(), key=lambda item: item.created_at, reverse=True)
        ]

    def get_run(self, run_id: str) -> AnalysisRunDetail:
        run = self._runs[run_id]
        return AnalysisRunDetail(
            run_id=run.run_id,
            analysis_type=run.analysis_type,
            client_id=run.client_id,
            account_id=run.account_id,
            created_at=run.created_at,
            input_payload=run.input_payload,
            findings_count=len(run.findings),
        )

    def get_findings(self, run_id: str) -> list[Finding]:
        return self._findings_by_run[run_id]

    def get_validation_issues(self, run_id: str) -> list[str]:
        return self._runs[run_id].validation_issues


run_store = AnalysisRunStore()
