# ADPILOT AI

AdPilot AI is a FastAPI-based advertising intelligence platform with deterministic analytics and evidence-bound AI interpretation.

## Features
- Provider-agnostic data interface with `mock_ads` and Windsor.ai adapter shell.
- Deterministic KPI, baseline comparison, anomaly detection, and campaign health scoring.
- Investigation workflow that separates facts, hypotheses, and evidence.
- Budget opportunity analysis with explicit uncertainty.
- Run history and finding validation endpoints.
- Synthetic fixture-backed end-to-end demo including CPA increase detection.

## Tech stack
Python 3.12+, FastAPI, Pydantic, Pandas, HTTPX, SQLAlchemy, Alembic, Pytest, Ruff.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
uvicorn app.main:app --reload
```

## Run checks
```bash
ruff check .
pytest
```

## Demo
```bash
python scripts/run_demo.py
```

## API
Swagger UI: `http://localhost:8000/docs`

Implemented endpoints:
- `GET /health`
- `GET /connectors`
- `GET /connectors/{connector}/fields`
- `POST /analysis/preview`
- `POST /analysis/campaign-health`
- `POST /analysis/investigate`
- `POST /analysis/budget-opportunities`
- `POST /assistant/ask`
- `GET /analysis/runs`
- `GET /analysis/runs/{run_id}`
- `GET /analysis/runs/{run_id}/findings`
- `POST /analysis/runs/{run_id}/validate`

## Notes on credentials
- Windsor.ai features require `WINDSOR_API_KEY`.
- LLM execution is mock-based in this initial implementation.












