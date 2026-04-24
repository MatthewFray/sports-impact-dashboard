"""First step toward a real NBA data ingestion layer for backend player data."""

from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models import Player, Team

try:
    from nba_api.stats.endpoints import commonteamroster
    from nba_api.stats.static import players, teams
except ImportError:  # pragma: no cover - depends on local environment
    commonteamroster = None
    players = None
    teams = None


def get_current_season_string() -> str:
    """Return the current NBA season in the format expected by nba_api."""
    from datetime import datetime

    today = datetime.now()
    start_year = today.year if today.month >= 7 else today.year - 1
    end_year = str(start_year + 1)[-2:]
    return f"{start_year}-{end_year}"


def get_denver_nuggets_team() -> dict[str, Any] | None:
    """Find the Denver Nuggets in the static nba_api teams dataset."""
    if teams is None:
        return None

    all_teams = teams.get_teams()
    return next(
        (
            team
            for team in all_teams
            if team["full_name"] == "Denver Nuggets"
            or team["abbreviation"] == "DEN"
        ),
        None,
    )


def get_current_players() -> list[dict[str, Any]]:
    """Return all active NBA players from the static nba_api dataset."""
    if players is None:
        return []

    return players.get_active_players()


def get_nuggets_roster(team_nba_id: int, season: str) -> list[dict[str, Any]]:
    """
    Fetch the current Nuggets roster if the endpoint is available.

    We use a live endpoint here because the static players dataset does not
    include team membership for active players.
    """
    if commonteamroster is None:
        return []

    roster_response = commonteamroster.CommonTeamRoster(
        team_id=team_nba_id,
        season=season,
    )
    roster_df = roster_response.get_data_frames()[0]
    return roster_df.to_dict(orient="records")


def print_team_preview(team_data: dict[str, Any]) -> None:
    """Print a readable summary of the Denver Nuggets team data."""
    print("\nDenver Nuggets team data from nba_api:")
    print(f"  NBA team id: {team_data['id']}")
    print(f"  Full name: {team_data['full_name']}")
    print(f"  Abbreviation: {team_data['abbreviation']}")
    print(f"  City: {team_data['city']}")
    print(f"  State: {team_data.get('state', 'N/A')}")
    print(f"  Year founded: {team_data.get('year_founded', 'N/A')}")


def print_players_preview(active_players: list[dict[str, Any]], roster_rows: list[dict[str, Any]]) -> None:
    """Print a readable preview of the active player pool and Nuggets roster."""
    print(f"\nActive NBA players found in static dataset: {len(active_players)}")
    print("Sample active players:")
    for player_row in active_players[:5]:
        print(f"  - {player_row['full_name']} (nba_player_id={player_row['id']})")

    if not roster_rows:
        print("\nNo Nuggets roster rows were retrieved from the endpoint.")
        return

    print(f"\nDenver Nuggets roster rows retrieved: {len(roster_rows)}")
    for roster_row in roster_rows:
        print(
            "  - "
            f"{roster_row.get('PLAYER', 'Unknown')} | "
            f"player_id={roster_row.get('PLAYER_ID')} | "
            f"number={roster_row.get('NUM', 'N/A')} | "
            f"position={roster_row.get('POSITION', 'N/A')}"
        )


def get_or_create_team(db: Session, team_data: dict[str, Any]) -> Team:
    """Find the Denver team in the database or create it if it does not exist."""
    existing_team = db.scalar(select(Team).where(Team.nba_team_id == team_data["id"]))
    if existing_team is not None:
        print(f"\nTeam already exists in database: {existing_team.name} (id={existing_team.id})")
        return existing_team

    team = Team(
        nba_team_id=team_data["id"],
        name=team_data["full_name"],
        abbreviation=team_data["abbreviation"],
        city=team_data["city"],
    )
    db.add(team)
    db.flush()
    print(f"\nCreated team in database: {team.name} (id={team.id})")
    return team


def build_player_payload(
    static_player: dict[str, Any],
    team_id: int,
    roster_row: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Map nba_api player data into fields supported by the current Player model."""
    full_name = static_player["full_name"]
    first_name = static_player["first_name"]
    last_name = static_player["last_name"]

    payload: dict[str, Any] = {
        "nba_player_id": static_player["id"],
        "first_name": first_name,
        "last_name": last_name,
        "full_name": full_name,
        "team_id": team_id,
        "jersey_number": roster_row.get("NUM") if roster_row else None,
        "position": roster_row.get("POSITION") if roster_row else None,
    }

    # The current Player model does not include an `is_active` column, so we do
    # not attempt to store that value yet.
    return payload


def insert_players(
    db: Session,
    team: Team,
    active_players: list[dict[str, Any]],
    roster_rows: list[dict[str, Any]],
) -> None:
    """Insert Nuggets players into the database without creating duplicates."""
    active_players_by_id = {player_row["id"]: player_row for player_row in active_players}
    roster_by_player_id = {
        int(roster_row["PLAYER_ID"]): roster_row
        for roster_row in roster_rows
        if roster_row.get("PLAYER_ID")
    }

    if not roster_by_player_id:
        print("\nRoster endpoint did not return player rows, so no players were inserted.")
        return

    inserted_count = 0
    skipped_count = 0

    for nba_player_id, roster_row in roster_by_player_id.items():
        static_player = active_players_by_id.get(nba_player_id)
        if static_player is None:
            print(
                f"  - Skipping player_id={nba_player_id}: not found in active static players dataset."
            )
            skipped_count += 1
            continue

        existing_player = db.scalar(select(Player).where(Player.nba_player_id == nba_player_id))
        if existing_player is not None:
            print(f"  - Skipping existing player: {existing_player.full_name} (id={existing_player.id})")
            skipped_count += 1
            continue

        player_payload = build_player_payload(
            static_player=static_player,
            team_id=team.id,
            roster_row=roster_row,
        )
        db.add(Player(**player_payload))
        inserted_count += 1
        print(f"  - Added player: {player_payload['full_name']}")

    print(f"\nInsert summary: inserted={inserted_count}, skipped={skipped_count}")


def import_nuggets_players() -> None:
    """Run the Denver Nuggets import flow from nba_api into the local database."""
    if teams is None or players is None:
        print("nba_api is not installed. Install it before running this script.")
        print("Example: pip install nba_api")
        return

    db = SessionLocal()

    try:
        season = get_current_season_string()
        team_data = get_denver_nuggets_team()
        if team_data is None:
            print("Denver Nuggets were not found in the static teams dataset.")
            return

        active_players = get_current_players()

        try:
            roster_rows = get_nuggets_roster(team_nba_id=team_data["id"], season=season)
        except Exception as roster_error:
            print("\nUnable to fetch Nuggets roster from nba_api endpoint.")
            print(f"Reason: {roster_error}")
            print("Continuing without inserts because player-to-team membership could not be confirmed.")
            roster_rows = []

        print_team_preview(team_data)
        print_players_preview(active_players=active_players, roster_rows=roster_rows)

        if not roster_rows:
            print("\nStopping before database inserts because no confirmed Nuggets roster was available.")
            return

        team = get_or_create_team(db, team_data)
        insert_players(
            db=db,
            team=team,
            active_players=active_players,
            roster_rows=roster_rows,
        )

        db.commit()
        print("\nImport completed successfully.")
    except Exception as exc:
        db.rollback()
        print("\nImport failed. Transaction rolled back.")
        print(f"Reason: {exc}")
        raise
    finally:
        db.close()
        print("Database session closed.")


if __name__ == "__main__":
    import_nuggets_players()
