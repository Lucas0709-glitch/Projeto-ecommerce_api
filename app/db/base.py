from datetime import datetime, timezone

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


def utcnow() -> datetime:
    """Data e hora atuais em UTC (substitui o datetime.utcnow, que foi descontinuado)."""
    return datetime.now(timezone.utc)