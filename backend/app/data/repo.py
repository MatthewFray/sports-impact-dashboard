from typing import List, Optional, Dict
from app.schemas.team import Team, TeamImpact, TeamImpactSummary
from app.data.store import TEAMS, IMPACTS

def list_teams(league: Optional[str] = None) -> List[Team]:
    if league:
        return [t for t in TEAMS if t.league.lower() == league.lower()]
    return TEAMS

def get_team(team_id: int) -> Optional[Team]:
    return next((t for t in TEAMS if t.id == team_id), None)

def team_exists(team_id: int) -> bool:
    return get_team(team_id) is not None

def get_team_impacts(team_id: int, season: Optional[int] = None) -> List[TeamImpact]:
    results = [x for x in IMPACTS if x.team_id == team_id]
    if season is not None:
        results = [x for x in results if x.season == season]
    return results

def get_team_impact_summary(team_id: int, season: int) -> Optional[TeamImpactSummary]:
    rows = [x for x in IMPACTS if x.team_id == team_id and x.season == season]
    if not rows:
        return None

    metrics: Dict[str, float] = {}
    for r in rows:
        metrics[r.metric] = metrics.get(r.metric, 0.0) + float(r.value)

    impact_score = sum(metrics.values())
    return TeamImpactSummary(team_id=team_id, season=season, metrics=metrics, impact_score=impact_score)