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

        variants = self._query_variants(query)
        async with httpx.AsyncClient(timeout=20.0) as client:
            for variant in variants:
                response = await client.get(
                    f"{settings.geocoding_base_url}/search",
                    params={"name": variant, "count": 8, "language": "en", "format": "json"},
                )
                response.raise_for_status()
                payload = response.json()
                results = payload.get("results") or []
                if results:
                    normalized = [self._normalize_result(item) for item in results]
                    return self._rank_results(query, normalized)

        raise LocationLookupError("No matching location was found", code="LOCATION_NOT_FOUND", status_code=404)

    async def resolve(self, query: str) -> LocationResult:
        return (await self.search(query))[0]

    async def reverse(self, lat: float, lon: float) -> LocationResult:
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise LocationLookupError("Coordinates are out of range", code="INVALID_COORDINATES")

        async with httpx.AsyncClient(timeout=20.0) as client:
            try:
                response = await client.get(
                    f"{settings.geocoding_base_url}/reverse",
                    params={"latitude": lat, "longitude": lon, "language": "en", "format": "json"},
                )
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                if exc.response.status_code == 404:
                    return self._coordinate_result(lat, lon)
                raise LocationLookupError("Location lookup failed", code="INVALID_LOCATION", status_code=502) from exc
            except httpx.HTTPError as exc:
                raise LocationLookupError("Location lookup failed", code="INVALID_LOCATION", status_code=502) from exc

        payload = response.json()
        results = payload.get("results") or []
        if results:
            return self._normalize_result(results[0])

        return self._coordinate_result(lat, lon)

    def _coordinate_result(self, lat: float, lon: float) -> LocationResult:
        label = f"{lat}, {lon}"
        return LocationResult(name=label, latitude=lat, longitude=lon, display_label=label)

    def _normalize_result(self, item: dict) -> LocationResult:
        region = item.get("admin1") or item.get("admin2")
        country = item.get("country")
        country_code = item.get("country_code")
        parts = [item.get("name"), region, country]
        label = ", ".join(part for part in parts if part)
        return LocationResult(
            name=item.get("name") or label,
            region=region,
            country=country,
            country_code=country_code.upper() if isinstance(country_code, str) else None,
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

    def _query_variants(self, query: str) -> list[str]:
        parts = [part.strip() for part in query.split(",") if part.strip()]
        variants = [query]
        if parts:
            variants.append(parts[0])
        seen = set()
        ordered = []
        for item in variants:
            lowered = item.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            ordered.append(item)
        return ordered

    def _rank_results(self, raw_query: str, results: list[LocationResult]) -> list[LocationResult]:
        query_parts = [part.strip().lower() for part in raw_query.split(",") if part.strip()]
        if len(query_parts) <= 1:
            return results

        def tokenize(value: str | None) -> set[str]:
            if not value:
                return set()
            normalized = value.lower().replace(",", " ").replace("-", " ")
            return {token for token in normalized.split() if token}

        def country_aliases(item: LocationResult) -> set[str]:
            aliases = tokenize(item.country)
            if item.country_code:
                aliases.add(item.country_code.lower())
            if item.country and item.country.lower() in {"united states", "united states of america"}:
                aliases.update({"us", "usa", "u.s.", "u.s.a.", "america"})
            if item.country and item.country.lower() == "united kingdom":
                aliases.update({"uk", "u.k.", "britain", "great britain"})
            return aliases

        def score(item: LocationResult) -> tuple[int, int, int, int]:
            item_name = (item.name or "").lower()
            exact_name = 1 if query_parts[0] == item_name else 0
            prefix_name = 1 if item_name.startswith(query_parts[0]) else 0
            general_tokens = tokenize(" ".join(filter(None, [item.name, item.region, item.country, item.display_label])))
            general_matches = sum(1 for part in query_parts if part in general_tokens)
            country_tokens = country_aliases(item)
            country_matches = sum(1 for part in query_parts[1:] if part in country_tokens)
            return (country_matches, exact_name, prefix_name, general_matches)

        return sorted(results, key=score, reverse=True)


location_service = LocationService()
