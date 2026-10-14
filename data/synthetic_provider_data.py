from datetime import date

SYNTHETIC_CONNECTOR_FIELDS = {
    "mock_ads": [
        "campaign_id",
        "campaign_name",
        "date",
        "currency",
        "spend",
        "clicks",
        "conversions",
        "impressions",
        "revenue",
    ]
}

SYNTHETIC_AUTHZ = {
    "user-1": {"client-a": {"acct-1"}},
    "user-2": {"client-b": {"acct-9"}},
}

SYNTHETIC_RECORDS = [
    {
        "campaign_id": "cmp-1",
        "campaign_name": "Search Brand",
        "date": date(2026, 9, 10),
        "currency": "USD",
        "spend": 100.0,
        "clicks": 120.0,
        "conversions": 10.0,
        "impressions": 2000.0,
        "revenue": 500.0,
    },
    {
        "campaign_id": "cmp-1",
        "campaign_name": "Search Brand",
        "date": date(2026, 10, 10),
        "currency": "USD",
        "spend": 160.0,
        "clicks": 130.0,
        "conversions": 8.0,
        "impressions": 2100.0,
        "revenue": 520.0,
    },
    {
        "campaign_id": "cmp-2",
        "campaign_name": "Prospecting Social",
        "date": date(2026, 9, 10),
        "currency": "USD",
        "spend": 200.0,
        "clicks": 190.0,
        "conversions": 7.0,
        "impressions": 5500.0,
        "revenue": 500.0,
    },
    {
        "campaign_id": "cmp-2",
        "campaign_name": "Prospecting Social",
        "date": date(2026, 10, 10),
        "currency": "USD",
        "spend": 260.0,
        "clicks": 180.0,
        "conversions": 6.0,
        "impressions": 5300.0,
        "revenue": 470.0,
    },
    {
        "campaign_id": "cmp-3",
        "campaign_name": "Display Retargeting",
        "date": date(2026, 9, 10),
        "currency": "EUR",
        "spend": 80.0,
        "clicks": 70.0,
        "conversions": 2.0,
        "impressions": 1400.0,
        "revenue": 200.0,
    },
    {
        "campaign_id": "cmp-3",
        "campaign_name": "Display Retargeting",
        "date": date(2026, 10, 10),
        "currency": "EUR",
        "spend": 90.0,
        "clicks": 75.0,
        "conversions": None,
        "impressions": 1500.0,
        "revenue": 205.0,
    },
]
