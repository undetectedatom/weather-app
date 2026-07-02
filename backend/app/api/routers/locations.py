from fastapi import APIRouter, HTTPException

from app.api.dependencies import SessionDep
from app.schemas.location import LocationSearchResponse
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
