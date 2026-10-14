from datetime import date

from data.synthetic_provider_data import SYNTHETIC_CONNECTOR_FIELDS, SYNTHETIC_RECORDS
from schemas.common import CampaignRecord

from .provider_interface import DataProvider


class MockDataProvider(DataProvider):
    async def get_connectors(self) -> list[dict[str, str]]:
        return [{"connector": "mock_ads", "description": "Synthetic fixture-backed ad connector"}]

    async def get_fields(self, connector: str) -> list[str]:
        return SYNTHETIC_CONNECTOR_FIELDS.get(connector, [])

    async def fetch_records(
        self,
        *,
        connector: str,
        account_id: str,
        start_date: date,
        end_date: date,
        fields: list[str],
    ) -> list[CampaignRecord]:
        if connector != "mock_ads":
            return []
        records = []
        for record in SYNTHETIC_RECORDS:
            if start_date <= record["date"] <= end_date:
                selected = {k: record.get(k) for k in fields if k in record}
                selected.update(
                    campaign_id=record["campaign_id"],
                    campaign_name=record["campaign_name"],
                    date=record["date"],
                )
                records.append(CampaignRecord(**selected))
        return records
