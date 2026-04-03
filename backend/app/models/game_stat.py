from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.player import Player


class GameStat(Base):
    __tablename__ = "game_stats"
    __table_args__ = (
        UniqueConstraint("player_id", "game_id", name="uq_game_stats_player_game"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
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

    player: Mapped["Player"] = relationship(back_populates="game_stats")
    game: Mapped["Game"] = relationship(back_populates="game_stats")


__all__ = ["GameStat"]
