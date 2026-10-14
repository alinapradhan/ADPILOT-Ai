from collections.abc import Mapping

REDACT_KEYS = {"authorization", "api_key", "token", "password", "secret"}


def redact_secrets(payload: Mapping[str, object]) -> dict[str, object]:
    redacted: dict[str, object] = {}
    for key, value in payload.items():
        if key.lower() in REDACT_KEYS:
            redacted[key] = "***REDACTED***"
        else:
            redacted[key] = value
    return redacted
