from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.game import Game
    from app.models.player import Player


class PlayerGameStat(Base):
    __tablename__ = "player_game_stats"
    __table_args__ = (
        UniqueConstraint("player_id", "game_id", name="uq_player_game_stats_player_game"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    player_id: Mapped[int] = mapped_column(ForeignKey("players.id"), index=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    minutes: Mapped[float | None] = mapped_column(Float)
    points: Mapped[int | None] = mapped_column(Integer)
    rebounds: Mapped[int | None] = mapped_column(Integer)
    assists: Mapped[int | None] = mapped_column(Integer)
    steals: Mapped[int | None] = mapped_column(Integer)
    blocks: Mapped[int | None] = mapped_column(Integer)
    turnovers: Mapped[int | None] = mapped_column(Integer)
    field_goal_pct: Mapped[float | None] = mapped_column(Float)
    three_point_pct: Mapped[float | None] = mapped_column(Float)
    free_throw_pct: Mapped[float | None] = mapped_column(Float)
    plus_minus: Mapped[int | None] = mapped_column(Integer)
    field_goals_made: Mapped[int | None] = mapped_column(Integer)
    field_goals_attempted: Mapped[int | None] = mapped_column(Integer)
    three_pointers_made: Mapped[int | None] = mapped_column(Integer)
    three_pointers_attempted: Mapped[int | None] = mapped_column(Integer)
    free_throws_made: Mapped[int | None] = mapped_column(Integer)
    free_throws_attempted: Mapped[int | None] = mapped_column(Integer)
    offensive_rebounds: Mapped[int | None] = mapped_column(Integer)
    defensive_rebounds: Mapped[int | None] = mapped_column(Integer)
    personal_fouls: Mapped[int | None] = mapped_column(Integer)

    player: Mapped["Player"] = relationship(back_populates="game_stats")
    game: Mapped["Game"] = relationship(back_populates="player_stats")


__all__ = ["PlayerGameStat"]
