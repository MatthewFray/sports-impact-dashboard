from pydantic import BaseModel
from typing import Optional, Dict

class Team(BaseModel):
    id: int
    name: str
    league: str
    city: Optional[str] = None

class TeamImpact(BaseModel):
    team_id: int
    season: int
    metric: str
    value: float

class TeamImpactSummary(BaseModel):
    team_id: int
    season: int
    metrics: Dict[str, float]
    impact_score: float