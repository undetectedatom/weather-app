from __future__ import annotations

import httpx

from app.schemas.location import LocationResult
from app.settings import settings


class LocationLookupError(Exception):
    def __init__(self, message: str, code: str = "INVALID_LOCATION", status_code: int = 400):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class LocationService:
    async def search(self, query: str) -> list[LocationResult]:
        query = query.strip()
        if not query:
            raise LocationLookupError("Location query cannot be empty")

        coordinates = self._parse_coordinates(query)
        if coordinates:
            lat, lon = coordinates
            return [LocationResult(name=f"{lat}, {lon}", latitude=lat, longitude=lon, display_label=f"{lat}, {lon}")]

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{settings.geocoding_base_url}/search",
                params={"name": query, "count": 5, "language": "en", "format": "json"},
            )
            response.raise_for_status()

        payload = response.json()
        results = payload.get("results") or []
        if not results:
            raise LocationLookupError("No matching location was found", code="LOCATION_NOT_FOUND", status_code=404)

        return [self._normalize_result(item) for item in results]

    async def resolve(self, query: str) -> LocationResult:
        return (await self.search(query))[0]

    async def reverse(self, lat: float, lon: float) -> LocationResult:
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise LocationLookupError("Coordinates are out of range", code="INVALID_COORDINATES")

        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.get(
                f"{settings.geocoding_base_url}/reverse",
                params={"latitude": lat, "longitude": lon, "language": "en", "format": "json"},
            )
            response.raise_for_status()

        payload = response.json()
        results = payload.get("results") or []
        if results:
            return self._normalize_result(results[0])

        return LocationResult(name=f"{lat}, {lon}", latitude=lat, longitude=lon, display_label=f"{lat}, {lon}")

    def _normalize_result(self, item: dict) -> LocationResult:
        region = item.get("admin1") or item.get("admin2")
        country = item.get("country")
        parts = [item.get("name"), region, country]
        label = ", ".join(part for part in parts if part)
        return LocationResult(
            name=item.get("name") or label,
            region=region,
            country=country,
            latitude=float(item["latitude"]),
            longitude=float(item["longitude"]),
            display_label=label,
        )

    def _parse_coordinates(self, query: str) -> tuple[float, float] | None:
        parts = [part.strip() for part in query.split(",")]
        if len(parts) != 2:
            return None
        try:
            lat = float(parts[0])
            lon = float(parts[1])
        except ValueError:
            return None
        if -90 <= lat <= 90 and -180 <= lon <= 180:
            return lat, lon
        raise LocationLookupError("Coordinates are out of range", code="INVALID_COORDINATES")


location_service = LocationService()
