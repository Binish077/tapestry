# Tapestry

An interactive family tree and royal archive for House Targaryen from the *Game of Thrones* universe.

## Technology Stack

- **Frontend:** TypeScript, React, and Vite
- **Backend:** Python, FastAPI, and SQLAlchemy
- **Database:** PostgreSQL

## Backend Database Setup

Create and activate the backend virtual environment, then install the project dependencies:

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r requirements.txt
```

Set `DATABASE_URL` in `backend/.env`. That file is ignored by Git. Apply the database schema from the backend directory:

```bash
cd backend
.venv/bin/alembic upgrade head
```

When models change, generate a migration and apply it:

```bash
.venv/bin/alembic revision --autogenerate -m "describe schema change"
.venv/bin/alembic upgrade head
```

## Seed Data

Load the starter House Targaryen dataset from `backend/data/seed.json` after applying the migrations:

```bash
cd backend
.venv/bin/python -m app.seed
```

The seed command is safe to rerun: it updates matching seed records and does not delete unrelated records. Edit the JSON file to add or change seed entities, relationships, and resources.

## Family Tree API

Start the FastAPI development server from the backend directory:

```bash
.venv/bin/uvicorn app.main:app --reload
```

The tree endpoint is available at `http://127.0.0.1:8000/api/tree`; interactive API documentation is at `http://127.0.0.1:8000/docs`.