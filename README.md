# Sports Impact Dashboard

## Project Overview
Sports Impact Dashboard is a prototype NBA analytics project focused on evaluating player impact beyond raw box score totals. The goal is to combine on-court production, salary context, and a future machine learning scoring layer into a backend and frontend system that is easy to extend and easy to explain.

## Current Features
- `nba_api` ingestion scripts for importing Denver Nuggets roster data and individual player data
- PostgreSQL-backed backend with SQLAlchemy models for players and teams
- Script-based ingestion pipeline for manually loading and expanding NBA data
- FastAPI player impact endpoint that returns normalized chart-ready metrics
- Basic React + TypeScript frontend foundation for displaying player impact data

## Architecture
The current data flow is:

`nba_api -> backend scripts/services -> PostgreSQL -> FastAPI API -> React frontend`

This keeps ingestion, storage, scoring, and presentation separated so the scoring system can evolve without changing the overall structure.

## Getting Started
### Run the backend
From the `backend` directory:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set `DATABASE_URL` if needed. The backend defaults to:

```bash
postgresql+psycopg://username:password@localhost:5432/database_name
```

### Run ingestion scripts
From the `backend` directory:

```bash
python -m app.scripts.import_nba_players
python -m app.scripts.import_single_player
```

You can also provide a player name to the single-player importer:

```bash
python -m app.scripts.import_single_player "Nikola Jokic"
```

### Run the frontend
From the `frontend` directory:

```bash
npm install
npm run dev
```

## Future Work
- Replace rule-based impact scoring with an ML-based scoring layer
- Expand ingestion beyond a single team and a single-player workflow
- Add stronger frontend visualizations such as radar or star charts
