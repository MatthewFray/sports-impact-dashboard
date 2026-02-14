from fastapi import APIRouter, Query
from typing import List, Optional
from app.schemas.team import Team, TeamImpact

router = APIRouter(tags=["teams"])

TEAMS = [
    Team(id=1, name="Denver Broncos", league="NFL", city="Denver"),
    Team(id=2, name="Denver Nuggets", league="NBA", city="Denver"),
    Team(id=3, name="Colorado Avalanche", league="NHL", city="Denver"),
]

IMPACTS = [
    TeamImpact(team_id=1, season=2023, metric="wins", value=8),
    TeamImpact(team_id=2, season=2023, metric="wins", value=57),
    TeamImpact(team_id=3, season=2023, metric="wins", value=50),
]

@router.get("/teams", response_model=List[Team])
def list_teams(league: Optional[str] = Query(default=None)):
    if league:
        return [t for t in TEAMS if t.league.lower() == league.lower()]
    return TEAMS

@router.get("/teams/{team_id}/impact", response_model=List[TeamImpact])
def get_team_impact(team_id: int, season: Optional[int] = None):
    results = [x for x in IMPACTS if x.team_id == team_id]
    if season is not None:
        results = [x for x in results if x.season == season]
    return results
