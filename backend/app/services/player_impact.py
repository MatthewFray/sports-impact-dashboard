from __future__ import annotations

from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Player


def clamp_score(value: float) -> int:
    """Clamp a score to the 0-100 range and return it as an integer."""
    return max(0, min(100, int(round(value))))


def normalize_stat(value: float, max_value: float) -> int:
    """Normalize a raw stat to a simple 0-100 score."""
    if max_value <= 0:
        return 0
    return clamp_score((value / max_value) * 100)


def calculate_ml_impact_score(player: Player) -> dict | None:
    # TODO: Replace rule-based scoring with ML model.
    return None


def _to_float(value: float | Decimal | None) -> float:
    """Convert numeric database values into a float safely."""
    if value is None:
        return 0.0
    return float(value)


def _calculate_contract_value_score(player: Player) -> int:
    """
    Estimate contract value using simple production-vs-salary logic.

    This is intentionally a readable placeholder so we can swap in a more
    advanced model later without changing the response shape.
    """
    production_score = (
        _to_float(player.points) * 1.0
        + _to_float(player.assists) * 1.5
        + _to_float(player.rebounds) * 1.2
        + _to_float(player.steals) * 2.0
        + _to_float(player.blocks) * 2.0
    )

    salary = _to_float(player.current_salary)
    if salary <= 0:
        return clamp_score(normalize_stat(production_score, 70.0))

    salary_in_millions = salary / 1_000_000
    value_ratio = production_score / max(salary_in_millions, 1.0)
    return normalize_stat(value_ratio, 3.0)


def get_player_impact_profile(db: Session, player_id: int) -> dict | None:
    """Return normalized star-chart metrics for one player."""
    player = db.get(Player, player_id)
    if player is None:
        return None

    efficiency_average = (
        _to_float(player.field_goal_pct)
        + _to_float(player.three_point_pct)
        + _to_float(player.free_throw_pct)
    ) / 3

    defense_total = _to_float(player.steals) + _to_float(player.blocks)

    metrics = [
        {"label": "Scoring", "value": normalize_stat(_to_float(player.points), 30.0)},
        {"label": "Efficiency", "value": normalize_stat(efficiency_average, 100.0)},
        {"label": "Playmaking", "value": normalize_stat(_to_float(player.assists), 12.0)},
        {"label": "Rebounding", "value": normalize_stat(_to_float(player.rebounds), 15.0)},
        {"label": "Defense", "value": normalize_stat(defense_total, 5.0)},
        {"label": "Contract Value", "value": _calculate_contract_value_score(player)},
    ]

    # Placeholder call to show where future ML logic can plug in.
    _ = calculate_ml_impact_score(player)

    return {
        "player_id": player.id,
        "player_name": player.full_name,
        "metrics": metrics,
        "metadata": {
            "model_version": "rule-based-v1",
            "uses_ml": False,
        },
    }


__all__ = [
    "calculate_ml_impact_score",
    "clamp_score",
    "get_player_impact_profile",
    "normalize_stat",
]
