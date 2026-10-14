PREVIEW_REQUEST = {
    "scope": {"client_id": "client-a", "account_id": "acct-1", "connector": "mock_ads"},
    "window": {
        "current_start": "2026-10-01",
        "current_end": "2026-10-31",
        "baseline_start": "2026-09-01",
        "baseline_end": "2026-09-30",
    },
}

INVESTIGATION_REQUEST = {
    **PREVIEW_REQUEST,
    "question": "Why did our cost per acquisition increase this month?",
}
