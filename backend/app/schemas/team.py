from pydantic import BaseModel
from typing import Optional

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
