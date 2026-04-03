from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.game_stat import GameStat


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    nba_game_id: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    season: Mapped[str] = mapped_column(String(20), index=True)
    game_date: Mapped[date] = mapped_column(Date, index=True)
    opponent: Mapped[str] = mapped_column(String(100))
    home_or_away: Mapped[str] = mapped_column(String(10))
    result: Mapped[str | None] = mapped_column(String(10))

    game_stats: Mapped[list["GameStat"]] = relationship(
        back_populates="game",
        cascade="all, delete-orphan",
    )


__all__ = ["Game"]
