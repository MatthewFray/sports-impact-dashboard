from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class Team:
    id: int
    name: str
    league: str
    city: Optional[str] = None


@dataclass
class TeamImpact:
    team_id: int
    season: int
    metric: str
    value: float


@dataclass
class TeamImpactSummary:
    team_id: int
    season: int
    metrics: Dict[str, float]
    impact_score: float
