from abc import ABC, abstractmethod
from datetime import date

from schemas.common import CampaignRecord


class DataProvider(ABC):
    @abstractmethod
    async def get_connectors(self) -> list[dict[str, str]]: ...

    @abstractmethod
    async def get_fields(self, connector: str) -> list[str]: ...

    @abstractmethod
    async def fetch_records(
        self,
        *,
        connector: str,
        account_id: str,
        start_date: date,
        end_date: date,
        fields: list[str],
    ) -> list[CampaignRecord]: ...
