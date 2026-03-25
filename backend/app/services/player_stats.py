from typing import Dict

from app.schemas.player import Player


def get_recent_x_game_averages(player: Player, x: int) -> Dict[str, float]:
    if x <= 0 or not player.game_stats:
        return {}

    recent_games = player.game_stats[:x]
    stat_fields = [
        "points",
        "assists",
        "rebounds",
        "steals",
        "blocks",
        "turnovers",
        "field_goal_pct",
        "three_point_pct",
        "free_throw_pct",
        "minutes",
    ]

    averages = {}
    total_games = len(recent_games)

    for field_name in stat_fields:
        total = sum(getattr(game, field_name) for game in recent_games)
        averages[field_name] = round(total / total_games, 2)

    return averages
