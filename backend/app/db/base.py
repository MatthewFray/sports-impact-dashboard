from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models."""


# Import models so SQLAlchemy registers them on Base.metadata for migrations.
from app.models import Game, Player, PlayerGameStat, Team  # noqa: E402,F401


__all__ = ["Base"]
