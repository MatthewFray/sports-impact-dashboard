from datetime import date, timedelta

from fastapi import APIRouter, HTTPException

from app.schemas.player import GameStat, Player
from app.services.player_stats import get_recent_x_game_averages

router = APIRouter(tags=["players"])


def _build_mock_player(player_id: int) -> Player:
    player = Player(
        player_id=player_id,
        first_name="Mock",
        last_name="Player",
        team="DEN",
        position="G",
        season="2025-26",
    )

    for index, stat_line in enumerate(
        [
            {"points": 28.0, "assists": 7.0, "rebounds": 6.0, "steals": 2.0, "blocks": 1.0, "turnovers": 3.0, "field_goal_pct": 52.4, "three_point_pct": 40.0, "free_throw_pct": 88.9, "minutes": 35.0},
            {"points": 22.0, "assists": 9.0, "rebounds": 5.0, "steals": 1.0, "blocks": 0.0, "turnovers": 2.0, "field_goal_pct": 47.8, "three_point_pct": 36.4, "free_throw_pct": 91.7, "minutes": 33.0},
            {"points": 31.0, "assists": 6.0, "rebounds": 8.0, "steals": 1.0, "blocks": 1.0, "turnovers": 4.0, "field_goal_pct": 55.1, "three_point_pct": 42.9, "free_throw_pct": 85.0, "minutes": 37.0},
            {"points": 18.0, "assists": 11.0, "rebounds": 4.0, "steals": 3.0, "blocks": 0.0, "turnovers": 1.0, "field_goal_pct": 44.0, "three_point_pct": 33.3, "free_throw_pct": 80.0, "minutes": 31.0},
            {"points": 26.0, "assists": 8.0, "rebounds": 7.0, "steals": 2.0, "blocks": 1.0, "turnovers": 2.0, "field_goal_pct": 50.0, "three_point_pct": 38.5, "free_throw_pct": 87.5, "minutes": 34.0},
        ]
    ):
        player.add_game_stat(
            GameStat(
                game_id=f"mock-game-{index + 1}",
                game_date=date.today() - timedelta(days=index),
                opponent=f"OPP{index + 1}",
                home_or_away="home" if index % 2 == 0 else "away",
                **stat_line,
            )
        )

    return player


@router.get("/players/{player_id}/recent-averages")
def get_player_recent_averages(player_id: int, games: int = 5):
    player = _build_mock_player(player_id)

    if not player.game_stats:
        raise HTTPException(status_code=404, detail="No game stats available")

    averages = get_recent_x_game_averages(player, games)

    return {
        "player_id": player_id,
        "player_name": player.full_name,
        "games_used": games,
        "averages": averages,
    }


__all__ = ["router"]
