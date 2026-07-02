from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import Session, col, select

from app.database.models import SnapshotType, User, WeatherHistory
from app.schemas.history import HistoryCreate, HistoryPublic, HistoryUpdate
from app.schemas.location import LocationResult
from app.services.location_service import LocationLookupError
from app.services.weather_service import WeatherServiceError, weather_service
from app.settings import settings


class HistoryError(Exception):
    def __init__(self, message: str, code: str = "RECORD_NOT_FOUND", status_code: int = 404):
        super().__init__(message)
        self.code = code
        self.status_code = status_code


class HistoryService:
    async def create_record(self, session: Session, user: User, payload: HistoryCreate) -> HistoryPublic:
        snapshot_type = self._snapshot_type(payload.start_date, payload.end_date)
        weather = await self._fetch_weather(payload.location, payload.start_date, payload.end_date)
        record = WeatherHistory(
            user_id=user.id,
            location_query=payload.location,
            resolved_name=weather.location.name,
            region=weather.location.region,
            country=weather.location.country,
            latitude=weather.location.latitude,
            longitude=weather.location.longitude,
            start_date=payload.start_date,
            end_date=payload.end_date,
            snapshot_type=snapshot_type,
            status=payload.status,
            notes=payload.notes,
            weather_payload=weather.model_dump(mode="json"),
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return HistoryPublic.model_validate(record)

    def list_records(self, session: Session, user: User) -> list[HistoryPublic]:
        statement = select(WeatherHistory).where(WeatherHistory.user_id == user.id).order_by(col(WeatherHistory.created_at).desc())
        return [HistoryPublic.model_validate(record) for record in session.exec(statement).all()]

    def get_record(self, session: Session, user: User, record_id: str) -> HistoryPublic:
        record = self._owned_record(session, user, record_id)
        return HistoryPublic.model_validate(record)

    async def update_record(self, session: Session, user: User, record_id: str, payload: HistoryUpdate) -> HistoryPublic:
        record = self._owned_record(session, user, record_id)
        next_location = payload.location or record.location_query
        next_start = payload.start_date if payload.start_date is not None else record.start_date
        next_end = payload.end_date if payload.end_date is not None else record.end_date

        if payload.location is not None or payload.start_date is not None or payload.end_date is not None:
            weather = await self._fetch_weather(next_location, next_start, next_end)
            record.location_query = next_location
            record.resolved_name = weather.location.name
            record.region = weather.location.region
            record.country = weather.location.country
            record.latitude = weather.location.latitude
            record.longitude = weather.location.longitude
            record.start_date = next_start
            record.end_date = next_end
            record.snapshot_type = self._snapshot_type(next_start, next_end)
            record.weather_payload = weather.model_dump(mode="json")

        if payload.status is not None:
            record.status = payload.status
        if payload.notes is not None:
            record.notes = payload.notes
        record.updated_at = datetime.now(timezone.utc)
        session.add(record)
        session.commit()
        session.refresh(record)
        return HistoryPublic.model_validate(record)

    def delete_record(self, session: Session, user: User, record_id: str) -> None:
        record = self._owned_record(session, user, record_id)
        session.delete(record)
        session.commit()

    def recent_locations(self, session: Session) -> list[LocationResult]:
        statement = select(WeatherHistory).order_by(col(WeatherHistory.created_at).desc())
        results: list[LocationResult] = []
        seen: set[tuple[float, float, str]] = set()
        for record in session.exec(statement):
            key = (record.latitude, record.longitude, record.resolved_name)
            if key in seen:
                continue
            seen.add(key)
            results.append(LocationResult(
                name=record.resolved_name,
                region=record.region,
                country=record.country,
                latitude=record.latitude,
                longitude=record.longitude,
                display_label=", ".join(part for part in [record.resolved_name, record.region, record.country] if part),
            ))
            if len(results) >= settings.recent_locations_limit:
                break
        return results

    def _owned_record(self, session: Session, user: User, record_id: str) -> WeatherHistory:
        try:
            parsed_id = UUID(record_id)
        except ValueError as exc:
            raise HistoryError("Record id is invalid", code="RECORD_NOT_FOUND", status_code=404) from exc
        record = session.exec(select(WeatherHistory).where(WeatherHistory.id == parsed_id, WeatherHistory.user_id == user.id)).first()
        if not record:
            raise HistoryError("Weather history record was not found")
        return record

    def _snapshot_type(self, start_date, end_date) -> SnapshotType:
        if start_date and end_date:
            return SnapshotType.range
        return SnapshotType.current

    async def _fetch_weather(self, location: str, start_date, end_date):
        try:
            if start_date and end_date:
                return await weather_service.get_range_weather(location, start_date.isoformat(), end_date.isoformat())
            return await weather_service.get_current_weather(location)
        except (LocationLookupError, WeatherServiceError) as exc:
            status_code = getattr(exc, "status_code", 400)
            code = getattr(exc, "code", "INVALID_LOCATION")
            raise HistoryError(str(exc), code=code, status_code=status_code) from exc


history_service = HistoryService()
