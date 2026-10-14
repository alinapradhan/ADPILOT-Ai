# Data Dictionary

Supported normalized fields:
- `campaign_id`, `campaign_name`, `date`, `currency`
- `spend`, `clicks`, `conversions`, `impressions`, `revenue`

Derived KPIs:
- `CPA = spend / conversions`
- `CTR = clicks / impressions`
- `CPC = spend / clicks`
- `ROAS = revenue / spend`

Unavailable values remain `null` and are not coerced to zero.
