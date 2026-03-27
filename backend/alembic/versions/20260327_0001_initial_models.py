"""create initial tables

Revision ID: 20260327_0001
Revises:
Create Date: 2026-03-27 03:05:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "20260327_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "games",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nba_game_id", sa.String(length=50), nullable=False),
        sa.Column("season", sa.String(length=20), nullable=False),
        sa.Column("game_date", sa.Date(), nullable=False),
        sa.Column("opponent", sa.String(length=100), nullable=False),
        sa.Column("home_or_away", sa.String(length=10), nullable=False),
        sa.Column("result", sa.String(length=10), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_games_game_date"), "games", ["game_date"], unique=False)
    op.create_index(op.f("ix_games_nba_game_id"), "games", ["nba_game_id"], unique=True)
    op.create_index(op.f("ix_games_season"), "games", ["season"], unique=False)

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nba_team_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("abbreviation", sa.String(length=10), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("abbreviation"),
        sa.UniqueConstraint("nba_team_id"),
    )
    op.create_index(op.f("ix_teams_abbreviation"), "teams", ["abbreviation"], unique=True)
    op.create_index(op.f("ix_teams_nba_team_id"), "teams", ["nba_team_id"], unique=True)

    op.create_table(
        "players",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nba_player_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("full_name", sa.String(length=200), nullable=False),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("jersey_number", sa.String(length=10), nullable=True),
        sa.Column("position", sa.String(length=25), nullable=True),
        sa.Column("salary", sa.Numeric(precision=12, scale=2), nullable=True),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nba_player_id"),
    )
    op.create_index(op.f("ix_players_full_name"), "players", ["full_name"], unique=False)
    op.create_index(op.f("ix_players_nba_player_id"), "players", ["nba_player_id"], unique=True)
    op.create_index(op.f("ix_players_team_id"), "players", ["team_id"], unique=False)

    op.create_table(
        "player_game_stats",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("player_id", sa.Integer(), nullable=False),
        sa.Column("game_id", sa.Integer(), nullable=False),
        sa.Column("minutes", sa.Float(), nullable=True),
        sa.Column("points", sa.Integer(), nullable=True),
        sa.Column("rebounds", sa.Integer(), nullable=True),
        sa.Column("assists", sa.Integer(), nullable=True),
        sa.Column("steals", sa.Integer(), nullable=True),
        sa.Column("blocks", sa.Integer(), nullable=True),
        sa.Column("turnovers", sa.Integer(), nullable=True),
        sa.Column("field_goal_pct", sa.Float(), nullable=True),
        sa.Column("three_point_pct", sa.Float(), nullable=True),
        sa.Column("free_throw_pct", sa.Float(), nullable=True),
        sa.Column("plus_minus", sa.Integer(), nullable=True),
        sa.Column("field_goals_made", sa.Integer(), nullable=True),
        sa.Column("field_goals_attempted", sa.Integer(), nullable=True),
        sa.Column("three_pointers_made", sa.Integer(), nullable=True),
        sa.Column("three_pointers_attempted", sa.Integer(), nullable=True),
        sa.Column("free_throws_made", sa.Integer(), nullable=True),
        sa.Column("free_throws_attempted", sa.Integer(), nullable=True),
        sa.Column("offensive_rebounds", sa.Integer(), nullable=True),
        sa.Column("defensive_rebounds", sa.Integer(), nullable=True),
        sa.Column("personal_fouls", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["game_id"], ["games.id"]),
        sa.ForeignKeyConstraint(["player_id"], ["players.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("player_id", "game_id", name="uq_player_game_stats_player_game"),
    )
    op.create_index(op.f("ix_player_game_stats_game_id"), "player_game_stats", ["game_id"], unique=False)
    op.create_index(op.f("ix_player_game_stats_player_id"), "player_game_stats", ["player_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_player_game_stats_player_id"), table_name="player_game_stats")
    op.drop_index(op.f("ix_player_game_stats_game_id"), table_name="player_game_stats")
    op.drop_table("player_game_stats")

    op.drop_index(op.f("ix_players_team_id"), table_name="players")
    op.drop_index(op.f("ix_players_nba_player_id"), table_name="players")
    op.drop_index(op.f("ix_players_full_name"), table_name="players")
    op.drop_table("players")

    op.drop_index(op.f("ix_teams_nba_team_id"), table_name="teams")
    op.drop_index(op.f("ix_teams_abbreviation"), table_name="teams")
    op.drop_table("teams")

    op.drop_index(op.f("ix_games_season"), table_name="games")
    op.drop_index(op.f("ix_games_nba_game_id"), table_name="games")
    op.drop_index(op.f("ix_games_game_date"), table_name="games")
    op.drop_table("games")
