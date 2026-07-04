# HelloWeather

HelloWeather is a full-stack weather application built for the PM Accelerator AI Engineer Intern technical assessment.

This submission covers both assessment tracks:
- Tech Assessment #1: frontend weather experience
- Tech Assessment #2: backend CRUD, persistence, export, and API integration

## What the project does

- Searches weather by city, zip code, landmark, or coordinates
- Uses current geolocation for local weather
- Shows current weather and a 5-day forecast
- Supports custom date-range weather queries with validation
- Stores weather history in SQLite with create, read, update, and delete flows
- Exports saved records as JSON, CSV, XML, and Markdown
- Includes location suggestions, OpenStreetMap preview, authentication, and dashboard management

## Stack

- Frontend: Vue 3 + Vite + Chart.js
- Backend: FastAPI + SQLModel + SQLite + httpx
- External APIs: Open-Meteo, OpenStreetMap Nominatim, OpenStreetMap embed

## Repo layout

- `frontend/` contains the Vue application
- `backend/` contains the FastAPI API, database models, and tests
- `docs/demo-video-script.md` contains a 1-2 minute demo script for the required walkthrough video

## Requirements

- Node.js `22.18.0+`
- Python `3.11+` is recommended

## Run locally

### Quick start from a fresh clone

Run these in two terminals from the repo root:

```bash
./start-backend.sh
./start-frontend.sh
```

The backend script creates `backend/.venv`, copies `backend/.env.example` to `backend/.env` when needed, installs Python dependencies, and starts FastAPI.

The frontend script installs `frontend/node_modules` when needed and starts Vite.

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The backend starts at `http://localhost:8000`.

### 2. Frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at `http://localhost:5173`.

If the backend runs on a different host or port, set `VITE_API_BASE_URL` before starting the frontend. The default value is `http://localhost:8000/api`.

## API summary

- `GET /api/weather/current`
- `GET /api/weather/forecast`
- `GET /api/weather/range`
- `GET /api/locations/search`
- `GET /api/locations/recent`
- `GET /api/locations/reverse`
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `POST /api/weather/history`
- `GET /api/weather/history`
- `GET /api/weather/history/{record_id}`
- `PATCH /api/weather/history/{record_id}`
- `DELETE /api/weather/history/{record_id}`
- `GET /api/weather/export?format=json|csv|xml|markdown`

## Notes for the assessment

- The app includes in-product PM Accelerator attribution plus author information in the UI.
- The demo script deliverable lives in `docs/demo-video-script.md`.
- The backend persists data in `backend/weather_app.db` by default.

## Verification

Backend tests:

```bash
cd backend
python -m pytest tests/test_api.py -vv
```

Frontend production build:

```bash
cd frontend
npm run build
```
