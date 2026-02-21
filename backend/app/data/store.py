from app.schemas.team import Team, TeamImpact

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