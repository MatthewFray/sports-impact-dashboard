from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Dict, List, Optional


@dataclass
class GameStat:
    game_id: str
    game_date: date
    opponent: str
    home_or_away: str
    points: float = 0.0
    assists: float = 0.0
    rebounds: float = 0.0
    steals: float = 0.0
    blocks: float = 0.0
    turnovers: float = 0.0
    field_goal_pct: float = 0.0
    three_point_pct: float = 0.0
    free_throw_pct: float = 0.0
    minutes: float = 0.0


@dataclass
class Player:
    player_id: int
    first_name: str
    last_name: str
    full_name: Optional[str] = None
    team: str = ""
    position: str = ""
    season: str = ""
    points: float = 0.0
    assists: float = 0.0
    rebounds: float = 0.0
    steals: float = 0.0
    blocks: float = 0.0
    turnovers: float = 0.0
    field_goal_pct: float = 0.0
    three_point_pct: float = 0.0
    free_throw_pct: float = 0.0
    minutes: float = 0.0
    game_stats: List[GameStat] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.full_name:
            self.full_name = self.get_full_name()

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    def to_dict(self) -> Dict:
        return asdict(self)

    def add_game_stat(self, game_stat: GameStat) -> None:
        self.game_stats.append(game_stat)
        self.game_stats.sort(key=lambda stat: stat.game_date, reverse=True)
