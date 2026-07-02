from fastapi import APIRouter

from app.api.routers.auth import router as auth_router
from app.api.routers.export import router as export_router
from app.api.routers.history import router as history_router
from app.api.routers.locations import router as locations_router
from app.api.routers.weather import router as weather_router

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(locations_router, prefix="/locations", tags=["locations"])
api_router.include_router(weather_router, prefix="/weather", tags=["weather"])
api_router.include_router(history_router, prefix="/weather/history", tags=["history"])
api_router.include_router(export_router, prefix="/weather/export", tags=["export"])
