from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from app.database.models import SnapshotType


class HistoryCreate(BaseModel):
    location: str
    start_date: date | None = None
    end_date: date | None = None
    status: str = "Saved"
    notes: str | None = None


class HistoryUpdate(BaseModel):
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None
    notes: str | None = None


class HistoryPublic(BaseModel):
    id: UUID
    user_id: UUID
    location_query: str
    resolved_name: str
    region: str | None = None
    country: str | None = None
    latitude: float
    longitude: float
    start_date: date | None = None
    end_date: date | None = None
    snapshot_type: SnapshotType
    status: str
    notes: str | None = None
    weather_payload: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HistoryListResponse(BaseModel):
    records: list[HistoryPublic]
