from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    env: str = Field(default="development")
    app_name: str = Field(default="AdPilot AI")
    api_prefix: str = Field(default="/")
    windsor_api_key: str | None = Field(default=None)
    llm_provider: str = Field(default="mock")
    database_url: str = Field(default="sqlite:///./adpilot.db")
    default_target_cpa: float = Field(default=40.0)
    default_target_roas: float = Field(default=2.5)


settings = Settings()
