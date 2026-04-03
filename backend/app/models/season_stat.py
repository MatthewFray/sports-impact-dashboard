from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.player import Player


class SeasonStat(Base):
    __tablename__ = "season_stats"
    __table_args__ = (
        UniqueConstraint("player_id", "season", name="uq_season_stats_player_season"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    season: Mapped[str] = mapped_column(String(20), index=True)
    salary: Mapped[Decimal | None] = mapped_column(Numeric(14, 2))
    minutes: Mapped[float] = mapped_column(Float, default=0.0)
    points: Mapped[float] = mapped_column(Float, default=0.0)
    rebounds: Mapped[float] = mapped_column(Float, default=0.0)
    assists: Mapped[float] = mapped_column(Float, default=0.0)
    steals: Mapped[float] = mapped_column(Float, default=0.0)
    blocks: Mapped[float] = mapped_column(Float, default=0.0)
    turnovers: Mapped[float] = mapped_column(Float, default=0.0)
    field_goal_pct: Mapped[float] = mapped_column(Float, default=0.0)
    three_point_pct: Mapped[float] = mapped_column(Float, default=0.0)
    free_throw_pct: Mapped[float] = mapped_column(Float, default=0.0)

    player: Mapped["Player"] = relationship(back_populates="season_stats")


__all__ = ["SeasonStat"]
