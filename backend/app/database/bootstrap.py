from sqlmodel import SQLModel

from app.database.engine import engine
from app.database.models import User, WeatherHistory


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
