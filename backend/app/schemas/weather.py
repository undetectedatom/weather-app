from pydantic import BaseModel

from app.schemas.location import LocationResult


class CurrentWeather(BaseModel):
    temperature_c: float
    feels_like_c: float | None = None
    condition: str
    humidity: float | None = None
    wind_speed: float | None = None
    temp_max_c: float | None = None
    temp_min_c: float | None = None
    icon_code: str


class ForecastDay(BaseModel):
    date: str
    temp_max_c: float | None = None
    temp_min_c: float | None = None
    condition: str
    icon_code: str


class RangeSummary(BaseModel):
    start_date: str
    end_date: str
    average_temp_c: float | None = None
    max_temp_c: float | None = None
    min_temp_c: float | None = None


class WeatherResponse(BaseModel):
    location: LocationResult
    current: CurrentWeather | None = None
    forecast_days: list[ForecastDay] = []
    range_summary: RangeSummary | None = None
    source: str = "open-meteo"
