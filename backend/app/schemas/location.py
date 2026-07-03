from pydantic import BaseModel


class LocationResult(BaseModel):
    name: str
    region: str | None = None
    country: str | None = None
    country_code: str | None = None
    latitude: float
    longitude: float
    display_label: str
    source: str = "open-meteo"


class LocationSearchResponse(BaseModel):
    results: list[LocationResult]
