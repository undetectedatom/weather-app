from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Weather App API"
    debug: bool = Field(default=False, alias="DEBUG")
    cors_origins: list[str] = Field(alias="BACKEND_CORS_ORIGINS")

    # @field_validator("cors_origins", mode="before")
    # @classmethod
    # def parse_array(cls, value: str) -> list[str]:
    #     raw = value.strip()
    #     if not raw:
    #         return []
    #     return [item.strip() for item in raw.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
