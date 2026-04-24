from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models import Game, GameStat, Player, SeasonStat, Team


def seed_data() -> None:
    db = SessionLocal()
    try:
        existing_team = db.scalar(
            select(Team).where(Team.abbreviation == "DEN")
        )
        if existing_team is not None:
            print("Seed skipped: Denver Nuggets already exist.")
            return

        team = Team(
            nba_team_id=1610612743,
            name="Denver Nuggets",
            abbreviation="DEN",
            city="Denver",
        )
        db.add(team)
        db.flush()

        player = Player(
            nba_player_id=203999,
            first_name="Nikola",
            last_name="Jokic",
            full_name="Nikola Jokic",
            team_id=team.id,
            jersey_number="15",
            position="C",
            current_salary=Decimal("51415938.00"),
            career_earnings=Decimal("203970494.00"),
            points=27.0,
            assists=10.0,
            rebounds=12.0,
            steals=1.0,
            blocks=1.0,
            turnovers=3.0,
            field_goal_pct=57.0,
            three_point_pct=33.3,
            free_throw_pct=83.3,
            minutes=35.0,
        )
        db.add(player)
        db.flush()

        season_stat = SeasonStat(
            player_id=player.id,
            season="2023-24",
            salary=Decimal("47607350.00"),
            points=27.0,
            assists=10.0,
            rebounds=12.0,
            steals=1.0,
            blocks=1.0,
            turnovers=3.0,
            field_goal_pct=57.0,
            three_point_pct=33.3,
            free_throw_pct=83.3,
            minutes=35.0,
        )
        db.add(season_stat)

        game = Game(
            nba_game_id="0022300001",
            season="2023-24",
            game_date=date(2023, 10, 24),
            opponent="Los Angeles Lakers",
            home_or_away="home",
            result="W",
        )
        db.add(game)
        db.flush()

        game_stat = GameStat(
            player_id=player.id,
            game_id=game.id,
            points=27.0,
            assists=10.0,
            rebounds=12.0,
            steals=1.0,
            blocks=1.0,
            turnovers=3.0,
            field_goal_pct=57.0,
            three_point_pct=33.3,
            free_throw_pct=83.3,
            minutes=35.0,
        )
        db.add(game_stat)

        db.commit()
        print("Seed data inserted successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
