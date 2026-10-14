# Security

- Connector credentials remain backend-only; secrets are redacted from logged request parameters.
- Scope authorization validates user-client-account relationships before data access.
- Numerical claims are validated against deterministic calculations.
- Retrieved ad text/content is treated as data, not instructions.
- The platform does not auto-apply budget or campaign changes.
