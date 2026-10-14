# Architecture

AdPilot AI uses independent modules:
- `integrations`: provider abstraction and connector adapters.
- `analytics`: deterministic normalization, KPI calculations, baseline comparison, anomaly detection, campaign health, and budget opportunities.
- `investigations` + `intelligence`: investigation planning, evidence assembly, orchestration, and response structuring.
- `llm`: interpretation layer with structured outputs.
- `validation`: claim validation for numerical support checks.
- `api`: authenticated endpoints over orchestrated services.

Deterministic analytics execute before interpretation. Findings explicitly separate facts and hypotheses and carry evidence references.
