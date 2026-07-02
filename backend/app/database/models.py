from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, List, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel


class SnapshotType(str, Enum):
    current = "current"
    forecast = "forecast"
    range = "range"


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    history_records: List["WeatherHistory"] = Relationship(back_populates="user")


class WeatherHistory(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    location_query: str
    resolved_name: str
    region: str | None = None
    country: str | None = None
    latitude: float
    longitude: float
    start_date: date | None = None
    end_date: date | None = None
    snapshot_type: SnapshotType
    status: str = "Saved"
    notes: str | None = None
    weather_payload: dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: Optional[User] = Relationship(back_populates="history_records")
