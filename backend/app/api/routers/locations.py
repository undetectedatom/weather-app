from fastapi import APIRouter, HTTPException, Query

from app.api.dependencies import SessionDep
from app.schemas.location import LocationResult, LocationSearchResponse
from app.services.history_service import history_service
from app.services.location_service import LocationLookupError, location_service

router = APIRouter()


@router.get("/search", response_model=LocationSearchResponse)
async def search_locations(query: str) -> LocationSearchResponse:
    try:
        results = await location_service.search(query)
    except LocationLookupError as exc:
        raise HTTPException(status_code=400, detail={"code": exc.code, "message": str(exc), "details": None}) from exc
    return LocationSearchResponse(results=results)


@router.get("/recent", response_model=LocationSearchResponse)
def recent_locations(session: SessionDep) -> LocationSearchResponse:
    return LocationSearchResponse(results=history_service.recent_locations(session))


@router.get("/reverse", response_model=LocationResult)
async def reverse_location(lat: float = Query(...), lon: float = Query(...)) -> LocationResult:
    try:
        return await location_service.reverse_name(lat, lon)
    except LocationLookupError as exc:
        raise HTTPException(status_code=exc.status_code, detail={"code": exc.code, "message": str(exc), "details": None}) from exc
