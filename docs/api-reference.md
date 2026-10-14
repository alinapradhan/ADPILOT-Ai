# API Reference

All endpoints require valid scope authorization via `X-User-Id` mapped to allowed `client_id` and `account_id`.

- `POST /analysis/*` endpoints accept `scope` and date windows.
- `POST /analysis/investigate` includes a user question and returns plan + findings.
- `POST /assistant/ask` consumes previously generated findings for concise prioritization.
- `POST /analysis/runs/{run_id}/validate` validates numerical support for run findings.

See `/docs` for full OpenAPI schema.
