from schemas.common import Finding


class LLMInterpreter:
    def interpret_findings(self, findings: list[Finding], question: str) -> str:
        if not findings:
            return (
                "No material change was detected from available evidence; request finer segmentation or longer windows."
            )
        prioritized = sorted(findings, key=lambda f: f.severity.value, reverse=True)
        top = prioritized[0]
        return (
            f"Question: {question}. Top observed change is {top.metric} with {top.description}. "
            "This is evidence-based and not a causal conclusion; additional breakdowns are required to confirm cause."
        )
