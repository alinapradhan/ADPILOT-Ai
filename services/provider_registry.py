from integrations.mock_provider import MockDataProvider
from integrations.provider_interface import DataProvider
from integrations.windsor_provider import WindsorDataProvider


class ProviderRegistry:
    def __init__(self) -> None:
        self.mock_provider = MockDataProvider()
        self.windsor_provider = WindsorDataProvider()

    def for_connector(self, connector: str) -> DataProvider:
        if connector == "windsor":
            return self.windsor_provider
        return self.mock_provider

    async def list_connectors(self) -> list[dict[str, str]]:
        connectors = await self.mock_provider.get_connectors()
        connectors.extend(await self.windsor_provider.get_connectors())
        return connectors


provider_registry = ProviderRegistry()
