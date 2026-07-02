from fastapi import APIRouter, HTTPException, Query

from app.schemas.weather import WeatherResponse
from app.services.location_service import LocationLookupError
from app.services.weather_service import WeatherServiceError, weather_service

router = APIRouter()


@router.get("/current", response_model=WeatherResponse)
async def get_current_weather(location: str) -> WeatherResponse:
    try:
        return await weather_service.get_current_weather(location)
    except (LocationLookupError, WeatherServiceError) as exc:
        raise HTTPException(status_code=exc.status_code if hasattr(exc, 'status_code') else 400, detail={"code": exc.code, "message": str(exc), "details": None}) from exc


@router.get("/current-location", response_model=WeatherResponse)
async def get_current_weather_for_coordinates(lat: float = Query(...), lon: float = Query(...)) -> WeatherResponse:
    try:
        return await weather_service.get_current_weather_by_coordinates(lat, lon)
    except WeatherServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc


@router.get("/forecast", response_model=WeatherResponse)
async def get_forecast(location: str, days: int = Query(default=5, ge=1, le=10)) -> WeatherResponse:
    try:
        return await weather_service.get_forecast(location, days)
    except (LocationLookupError, WeatherServiceError) as exc:
        raise HTTPException(status_code=exc.status_code if hasattr(exc, 'status_code') else 400, detail={"code": exc.code, "message": str(exc), "details": None}) from exc


@router.get("/range", response_model=WeatherResponse)
async def get_range_weather(location: str, start_date: str, end_date: str) -> WeatherResponse:
    try:
        return await weather_service.get_range_weather(location, start_date, end_date)
    except (LocationLookupError, WeatherServiceError) as exc:
        raise HTTPException(status_code=exc.status_code if hasattr(exc, 'status_code') else 400, detail={"code": exc.code, "message": str(exc), "details": None}) from exc
