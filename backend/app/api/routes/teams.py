from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from app.schemas.team import Team, TeamImpact, TeamImpactSummary

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
    if not any(t.id == team_id for t in TEAMS):
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    results = [x for x in IMPACTS if x.team_id == team_id]
    if season is not None:
        results = [x for x in results if x.season == season]
    return results

@router.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):
    for t in TEAMS:
        if t.id == team_id:
            return t
    raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

@router.get("/teams/{team_id}/impact/summary", response_model=TeamImpactSummary)
def get_team_impact_summary(team_id: int, season: int = Query(...)):
    if not any(t.id == team_id for t in TEAMS):
        raise HTTPException(status_code=404, detail=f"Team {team_id} not found")

    rows = [x for x in IMPACTS if x.team_id == team_id and x.season == season]
    if not rows:
        raise HTTPException(status_code=404, detail=f"No impact data for team {team_id} in season {season}")

    metrics = {}
    for r in rows:
        metrics[r.metric] = metrics.get(r.metric, 0) + float(r.value)

    impact_score = sum(metrics.values())

    return TeamImpactSummary(team_id=team_id, season=season, metrics=metrics, impact_score=impact_score)