from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional

from app.schemas.team import Team, TeamImpact, TeamImpactSummary
from app.data import repo

router = APIRouter(tags=["teams"])

@router.get("/teams", response_model=List[Team])
def list_teams(league: Optional[str] = Query(default=None)):
    return repo.list_teams(league=league)

@router.get("/teams/{team_id}/impact", response_model=List[TeamImpact])
def get_team_impact(team_id: int, season: Optional[int] = None):
    if not repo.team_exists(team_id):
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
    return repo.get_team_impacts(team_id=team_id, season=season)

@router.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    team = repo.get_team(team_id)
    if team is None:
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")
    return team

@router.get("/teams/{team_id}/impact/summary", response_model=TeamImpactSummary)
def get_team_impact_summary(team_id: int, season: int = Query(...)):
    if not repo.team_exists(team_id):
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    summary = repo.get_team_impact_summary(team_id=team_id, season=season)
    if summary is None:
        raise HTTPException(status_code=404, detail=f"No impact data for team {team_id} in season {season}")

    return summary