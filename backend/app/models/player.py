from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.player_game_stat import PlayerGameStat
    from app.models.team import Team


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    nba_player_id: Mapped[int] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    full_name: Mapped[str] = mapped_column(String(200), index=True)
    team_id: Mapped[int | None] = mapped_column(ForeignKey("teams.id"), index=True)
    jersey_number: Mapped[str | None] = mapped_column(String(10))
    position: Mapped[str | None] = mapped_column(String(25))
    salary: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    team: Mapped["Team | None"] = relationship(back_populates="players")
    game_stats: Mapped[list["PlayerGameStat"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )


__all__ = ["Player"]
