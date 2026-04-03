from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.game_stat import GameStat
    from app.models.season_stat import SeasonStat
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
    current_salary: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    career_earnings: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    points: Mapped[float] = mapped_column(Float, default=0.0)
    assists: Mapped[float] = mapped_column(Float, default=0.0)
    rebounds: Mapped[float] = mapped_column(Float, default=0.0)
    steals: Mapped[float] = mapped_column(Float, default=0.0)
    blocks: Mapped[float] = mapped_column(Float, default=0.0)
    turnovers: Mapped[float] = mapped_column(Float, default=0.0)
    field_goal_pct: Mapped[float] = mapped_column(Float, default=0.0)
    three_point_pct: Mapped[float] = mapped_column(Float, default=0.0)
    free_throw_pct: Mapped[float] = mapped_column(Float, default=0.0)
    minutes: Mapped[float] = mapped_column(Float, default=0.0)

    team: Mapped["Team | None"] = relationship(back_populates="players")
    season_stats: Mapped[list["SeasonStat"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )
    game_stats: Mapped[list["GameStat"]] = relationship(
        back_populates="player",
        cascade="all, delete-orphan",
    )


__all__ = ["Player"]
