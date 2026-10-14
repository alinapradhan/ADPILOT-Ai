from datetime import date

import httpx

from core.config import settings
from core.errors import DataProviderError
from core.logging import redact_secrets
from schemas.common import CampaignRecord

from .provider_interface import DataProvider


class WindsorDataProvider(DataProvider):
    base_url = "https://api.windsor.ai"

    async def get_connectors(self) -> list[dict[str, str]]:
        if not settings.windsor_api_key:
            return []
        return [{"connector": "windsor", "description": "Windsor.ai connector (requires credentials)"}]

    async def get_fields(self, connector: str) -> list[str]:
        if connector != "windsor":
            return []
        return ["campaign", "date", "spend", "clicks", "conversions", "impressions", "revenue"]

    async def fetch_records(
        self,
        *,
        connector: str,
        account_id: str,
        start_date: date,
        end_date: date,
        fields: list[str],
    ) -> list[CampaignRecord]:
        if connector != "windsor":
            return []
        if not settings.windsor_api_key:
            raise DataProviderError("Windsor.ai credentials are not configured")

        params = {
            "api_key": settings.windsor_api_key,
            "account": account_id,
            "date_from": start_date.isoformat(),
            "date_to": end_date.isoformat(),
            "fields": ",".join(fields),
        }
        safe_params = redact_secrets(params)
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(f"{self.base_url}/v1/reporting", params=params)
                response.raise_for_status()
        except (httpx.HTTPStatusError, httpx.RequestError) as exc:
            raise DataProviderError(f"Windsor.ai request failed with params={safe_params}") from exc

        rows = response.json() if isinstance(response.json(), list) else []
        records: list[CampaignRecord] = []
        for row in rows:
            records.append(
                CampaignRecord(
                    campaign_id=str(row.get("campaign", "unknown")),
                    campaign_name=str(row.get("campaign", "unknown")),
                    date=date.fromisoformat(str(row.get("date"))),
                    currency=str(row.get("currency", "USD")),
                    spend=row.get("spend"),
                    clicks=row.get("clicks"),
                    conversions=row.get("conversions"),
                    impressions=row.get("impressions"),
                    revenue=row.get("revenue"),
                )
            )
        return records
