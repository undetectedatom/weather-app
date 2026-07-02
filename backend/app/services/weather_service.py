from __future__ import annotations

from datetime import date, datetime, timezone
from statistics import mean

import httpx

from app.schemas.weather import CurrentWeather, ForecastDay, RangeSummary, WeatherResponse
from app.services.location_service import location_service
from app.settings import settings

WEATHER_CODES = {
    0: ("Clear sky", "clear"),
    1: ("Mainly clear", "partly-cloudy"),
    2: ("Partly cloudy", "partly-cloudy"),
    3: ("Overcast", "cloudy"),
    45: ("Fog", "fog"),
    48: ("Depositing rime fog", "fog"),
    51: ("Light drizzle", "drizzle"),
    53: ("Moderate drizzle", "drizzle"),
    55: ("Dense drizzle", "drizzle"),
    61: ("Slight rain", "rain"),
    63: ("Moderate rain", "rain"),
    65: ("Heavy rain", "rain"),
    71: ("Slight snow", "snow"),
    80: ("Rain showers", "showers"),
    95: ("Thunderstorm", "storm"),
}


class WeatherServiceError(Exception):
    def __init__(self, message: str, code: str = "UPSTREAM_WEATHER_ERROR", status_code: int = 502):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class WeatherService:
    async def get_current_weather(self, query: str) -> WeatherResponse:
        location = await location_service.resolve(query)
        return await self.get_current_weather_by_coordinates(location.latitude, location.longitude, location)

    async def get_current_weather_by_coordinates(self, lat: float, lon: float, resolved_location=None) -> WeatherResponse:
        location = resolved_location or await location_service.reverse(lat, lon)
        payload = await self._fetch_forecast(lat, lon, forecast_days=1)
        current = payload.get("current") or {}
        return WeatherResponse(
            location=location,
            current=CurrentWeather(
                temperature_c=float(current.get("temperature_2m", 0.0)),
                feels_like_c=float(current["apparent_temperature"]) if current.get("apparent_temperature") is not None else None,
                condition=self._condition(current.get("weather_code"))[0],
                humidity=float(current["relative_humidity_2m"]) if current.get("relative_humidity_2m") is not None else None,
                wind_speed=float(current["wind_speed_10m"]) if current.get("wind_speed_10m") is not None else None,
                icon_code=self._condition(current.get("weather_code"))[1],
            ),
            forecast_days=[],
        )

    async def get_forecast(self, query: str, days: int) -> WeatherResponse:
        location = await location_service.resolve(query)
        payload = await self._fetch_forecast(location.latitude, location.longitude, forecast_days=days)
        daily = payload.get("daily") or {}
        return WeatherResponse(
            location=location,
            current=None,
            forecast_days=self._build_forecast_days(daily),
        )

    async def get_range_weather(self, query: str, start_date_raw: str, end_date_raw: str) -> WeatherResponse:
        start_date, end_date = self._validate_range(start_date_raw, end_date_raw)
        location = await location_service.resolve(query)
        today = datetime.now(timezone.utc).date()
        if start_date > today or end_date > today:
            raise WeatherServiceError("Future date ranges are not supported by the selected provider", code="INVALID_DATE_RANGE", status_code=400)

        payload = await self._fetch_archive(location.latitude, location.longitude, start_date.isoformat(), end_date.isoformat())
        daily = payload.get("daily") or {}
        forecast_days = self._build_forecast_days(daily)
        max_values = daily.get("temperature_2m_max") or []
        min_values = daily.get("temperature_2m_min") or []
        avg_values = [(high + low) / 2 for high, low in zip(max_values, min_values)]
        return WeatherResponse(
            location=location,
            forecast_days=forecast_days,
            range_summary=RangeSummary(
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                average_temp_c=round(mean(avg_values), 2) if avg_values else None,
                max_temp_c=max(max_values) if max_values else None,
                min_temp_c=min(min_values) if min_values else None,
            ),
            current=None,
        )

    async def _fetch_forecast(self, lat: float, lon: float, forecast_days: int) -> dict:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": ["temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m", "weather_code"],
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
            "timezone": "auto",
            "forecast_days": forecast_days,
        }
        return await self._request(f"{settings.weather_base_url}/forecast", params)

    async def _fetch_archive(self, lat: float, lon: float, start_date: str, end_date: str) -> dict:
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min"],
            "timezone": "auto",
        }
        return await self._request("https://archive-api.open-meteo.com/v1/archive", params)

    async def _request(self, url: str, params: dict) -> dict:
        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(url, params=params)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                raise WeatherServiceError("Weather provider request failed") from exc
        return response.json()

    def _build_forecast_days(self, daily: dict) -> list[ForecastDay]:
        times = daily.get("time") or []
        codes = daily.get("weather_code") or []
        max_values = daily.get("temperature_2m_max") or []
        min_values = daily.get("temperature_2m_min") or []
        items: list[ForecastDay] = []
        for index, weather_date in enumerate(times):
            label, icon = self._condition(codes[index] if index < len(codes) else None)
            items.append(ForecastDay(
                date=weather_date,
                temp_max_c=max_values[index] if index < len(max_values) else None,
                temp_min_c=min_values[index] if index < len(min_values) else None,
                condition=label,
                icon_code=icon,
            ))
        return items

    def _condition(self, code: int | None) -> tuple[str, str]:
        return WEATHER_CODES.get(code, ("Unknown", "unknown"))

    def _validate_range(self, start_date_raw: str, end_date_raw: str) -> tuple[date, date]:
        try:
            start_date = date.fromisoformat(start_date_raw)
            end_date = date.fromisoformat(end_date_raw)
        except ValueError as exc:
            raise WeatherServiceError("Dates must use YYYY-MM-DD format", code="INVALID_DATE_RANGE", status_code=400) from exc
        if start_date > end_date:
            raise WeatherServiceError("Start date must be before or equal to end date", code="INVALID_DATE_RANGE", status_code=400)
        return start_date, end_date


weather_service = WeatherService()
