from __future__ import annotations

import csv
from pathlib import Path


def load_player_stats(csv_path: Path) -> list[dict[str, str]]:
    """Load player stats from a CSV file into a list of dictionaries."""
    with csv_path.open(mode="r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


def print_player_stats(player_stats: list[dict[str, str]]) -> None:
    """Print each player's stats in a readable format."""
    for player in player_stats:
        print(
            f"{player['player_name']} ({player['team']}): "
            f"{player['points']} PPG, "
            f"{player['assists']} APG, "
            f"{player['rebounds']} RPG"
        )


def main() -> None:
    # Build a stable path so the script works no matter where it is run from.
    csv_path = Path(__file__).resolve().parents[1] / "app" / "data" / "player_stats.csv"
    player_stats = load_player_stats(csv_path)
    print_player_stats(player_stats)


if __name__ == "__main__":
    main()
