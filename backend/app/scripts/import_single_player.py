"""Smaller NBA ingestion script for testing one player before scaling to team imports."""

from __future__ import annotations

import sys
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Player

DEFAULT_PLAYER_NAME = "Nikola Jokic"

try:
    from nba_api.stats.endpoints import playercareerstats
    from nba_api.stats.static import players
except ImportError:  # pragma: no cover - depends on local environment
    playercareerstats = None
    players = None


def find_player_by_name(player_name: str) -> dict[str, Any] | None:
    """Find a single NBA player from the static nba_api player dataset."""
    if players is None:
        return None

    matches = players.find_players_by_full_name(player_name)
    if not matches:
        return None

    exact_match = next(
        (
            player_row
            for player_row in matches
            if player_row["full_name"].lower() == player_name.lower()
        ),
        None,
    )
    return exact_match or matches[0]


def get_player_career_stats(nba_player_id: int) -> list[dict[str, Any]]:
    """Fetch career stats rows for a single player using nba_api."""
    if playercareerstats is None:
        return []

    career_stats_response = playercareerstats.PlayerCareerStats(player_id=nba_player_id)
    career_stats_df = career_stats_response.get_data_frames()[0]
    return career_stats_df.to_dict(orient="records")


def get_latest_season_stats(career_stat_rows: list[dict[str, Any]]) -> dict[str, Any] | None:
    """
    Return the latest usable season row for the player.

    The endpoint usually returns one row per season plus summary rows like
    "Career". We skip non-season labels and choose the most recent season row.
    """
    season_rows = [
        row for row in career_stat_rows if isinstance(row.get("SEASON_ID"), str) and "-" in row["SEASON_ID"]
    ]
    if not season_rows:
        return None

    return sorted(season_rows, key=lambda row: row["SEASON_ID"])[-1]


def print_player_preview(
    player_data: dict[str, Any],
    career_stat_rows: list[dict[str, Any]],
    latest_season_stats: dict[str, Any] | None,
) -> None:
    """Print a readable preview before any database insert happens."""
    print("\nSingle player preview from nba_api:")
    print(f"  Player name: {player_data['full_name']}")
    print(f"  NBA player id: {player_data['id']}")
    print(f"  Active status: {player_data.get('is_active', 'N/A')}")
    print(f"  Career/season stat rows available: {len(career_stat_rows)}")

    if latest_season_stats is None:
        print("  Latest season stats: not available")
        return

    print("\nLatest season stats preview:")
    print(f"  Season: {latest_season_stats.get('SEASON_ID', 'N/A')}")
    print(f"  Team id from stats row: {latest_season_stats.get('TEAM_ID', 'N/A')}")
    print(f"  Games played: {latest_season_stats.get('GP', 'N/A')}")
    print(f"  Points per game: {latest_season_stats.get('PTS', 'N/A')}")
    print(f"  Assists per game: {latest_season_stats.get('AST', 'N/A')}")
    print(f"  Rebounds per game: {latest_season_stats.get('REB', 'N/A')}")
    print(f"  Minutes per game: {latest_season_stats.get('MIN', 'N/A')}")


def build_player_payload(
    player_data: dict[str, Any],
    latest_season_stats: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build a Player payload using only fields supported by the current model."""
    payload: dict[str, Any] = {
        "nba_player_id": player_data["id"],
        "first_name": player_data["first_name"],
        "last_name": player_data["last_name"],
        "full_name": player_data["full_name"],
        "team_id": None,
        "current_salary": None,
        "career_earnings": None,
    }

    # The current Player model does not include an `is_active` column, so we
    # preview it in the console but do not store it in the database yet.
    if latest_season_stats is None:
        return payload

    payload.update(
        {
            "points": float(latest_season_stats.get("PTS") or 0.0),
            "assists": float(latest_season_stats.get("AST") or 0.0),
            "rebounds": float(latest_season_stats.get("REB") or 0.0),
            "steals": float(latest_season_stats.get("STL") or 0.0),
            "blocks": float(latest_season_stats.get("BLK") or 0.0),
            "turnovers": float(latest_season_stats.get("TOV") or 0.0),
            "field_goal_pct": float(latest_season_stats.get("FG_PCT") or 0.0),
            "three_point_pct": float(latest_season_stats.get("FG3_PCT") or 0.0),
            "free_throw_pct": float(latest_season_stats.get("FT_PCT") or 0.0),
            "minutes": float(latest_season_stats.get("MIN") or 0.0),
        }
    )

    # We intentionally leave `team_id` as None here. A single player lookup does
    # not guarantee a safe current-team match against the local Team table.
    return payload


def insert_single_player(
    db: Session,
    player_data: dict[str, Any],
    latest_season_stats: dict[str, Any] | None,
) -> None:
    """Insert one player into the database if the player does not already exist."""
    existing_player = db.scalar(select(Player).where(Player.nba_player_id == player_data["id"]))
    if existing_player is not None:
        print(f"\nPlayer already exists in database: {existing_player.full_name} (id={existing_player.id})")
        return

    player_payload = build_player_payload(
        player_data=player_data,
        latest_season_stats=latest_season_stats,
    )
    db.add(Player(**player_payload))
    print(f"\nInserted player into database: {player_payload['full_name']}")


def import_single_player(player_name: str = DEFAULT_PLAYER_NAME) -> None:
    """Run the single-player import flow for a player such as Nikola Jokic."""
    if players is None:
        print("nba_api is not installed. Install it before running this script.")
        print("Example: pip install nba_api")
        return

    db = SessionLocal()

    try:
        player_data = find_player_by_name(player_name)
        if player_data is None:
            print(f"Player not found in nba_api static dataset: {player_name}")
            return

        try:
            career_stat_rows = get_player_career_stats(player_data["id"])
        except Exception as stats_error:
            print("\nUnable to fetch player career stats from nba_api.")
            print(f"Reason: {stats_error}")
            career_stat_rows = []

        latest_season_stats = get_latest_season_stats(career_stat_rows)

        print_player_preview(
            player_data=player_data,
            career_stat_rows=career_stat_rows,
            latest_season_stats=latest_season_stats,
        )

        insert_single_player(
            db=db,
            player_data=player_data,
            latest_season_stats=latest_season_stats,
        )

        db.commit()
        print("\nSingle-player import completed successfully.")
    except Exception as exc:
        db.rollback()
        print("\nSingle-player import failed. Transaction rolled back.")
        print(f"Reason: {exc}")
        raise
    finally:
        db.close()
        print("Database session closed.")


def main() -> None:
    """Allow running the script with an optional player name argument."""
    player_name = " ".join(sys.argv[1:]).strip() or DEFAULT_PLAYER_NAME
    import_single_player(player_name=player_name)


if __name__ == "__main__":
    main()
