from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Weather App API"
    debug: bool = Field(default=False, alias="DEBUG")
    cors_origins: list[str] = Field(default=["http://localhost:5173", "http://localhost:8080"], alias="BACKEND_CORS_ORIGINS")
    database_url: str = Field(default="sqlite:///./weather_app.db", alias="DATABASE_URL")
    cookie_name: str = Field(default="weather_app_auth", alias="AUTH_COOKIE_NAME")
    cookie_secret: str = Field(default="change-me-in-production", alias="AUTH_COOKIE_SECRET")
    cookie_secure: bool = Field(default=False, alias="AUTH_COOKIE_SECURE")
    cookie_samesite: str = Field(default="lax", alias="AUTH_COOKIE_SAMESITE")
    weather_base_url: str = Field(default="https://api.open-meteo.com/v1", alias="OPEN_METEO_BASE_URL")
    geocoding_base_url: str = Field(default="https://geocoding-api.open-meteo.com/v1", alias="OPEN_METEO_GEOCODING_BASE_URL")
    osm_geocoding_base_url: str = Field(default="https://nominatim.openstreetmap.org", alias="OSM_GEOCODING_BASE_URL")
    forecast_days: int = Field(default=5, alias="FORECAST_DAYS_DEFAULT")
    recent_locations_limit: int = Field(default=5, alias="RECENT_LOCATIONS_LIMIT")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
