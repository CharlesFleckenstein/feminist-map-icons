# Gallery of Possibilities

A feminist map icon gallery website and API for the QGIS plugin.

This repo is a place to store, browse, upload, and manage map icons. The website and the QGIS plugin will both use the same backend.

## Team

| Area | Focus |
|------|--------|
| Backend / database | Django, PostgreSQL, APIs, file storage |
| Frontend | React UI, gallery, forms, pages |

## Stack

- **Frontend:** React (Vite)
- **Backend:** Django + Django REST Framework
- **Database:** PostgreSQL

## Repo layout

| Path | Purpose |
|------|---------|
| `backend/` | Django API and admin |
| `backend/data/` | Shared icon metadata CSV (safe to commit) |
| `backend/media/` | Local PNG/SVG files after import (do **not** commit) |
| `frontend/` | React app |

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL

## Backend setup

### 1. Create the database

In pgAdmin (or `psql`), create a PostgreSQL database named `gop`.

### 2. Configure environment variables

```bash
cd backend
copy .env.example .env
```

On macOS/Linux use `cp .env.example .env` instead.

Edit `.env` and set:

- `SECRET_KEY` — any long random string
- `DB_PASSWORD` — your local PostgreSQL password
- `DB_USER` — usually `postgres` (change if you use another user)

Do **not** commit `.env`.

### 3. Install dependencies and run

```bash
cd backend
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**macOS / Linux:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will be at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Import existing icons (one-time)

### 1. Metadata CSV (already in the repo)

```text
backend/data/map-icon-metadata.csv
```

### 2. Download PNG and SVG folders

Get the icon folders from the Zenodo export [https://zenodo.org/records/22134192]. You need two folders of files named by `unique-ID`, for example:

- `map-icon-png/` → `00e8059e.png`, `021fd014.png`, …
- `map-icon-svg/` → `00e8059e.svg`, `021fd014.svg`, …

Put them anywhere on your computer (Downloads is fine).

### 3. Run the import

From `backend/` with your venv active:

**Windows (PowerShell):**

```powershell
python manage.py import_icons --csv data/map-icon-metadata.csv --png "C:\Users\YOUR_NAME\Downloads\map-icon-png" --svg "C:\Users\YOUR_NAME\Downloads\map-icon-svg"
```

**macOS / Linux:**

```bash
python manage.py import_icons --csv data/map-icon-metadata.csv --png ~/Downloads/map-icon-png --svg ~/Downloads/map-icon-svg
```

You should see something like `Created 209` .

### 4. Check

[http://127.0.0.1:8000/api/icons/](http://127.0.0.1:8000/api/icons/).

## Frontend setup

Requires Node.js 18+. The Vite proxy is already configured so `/api` and `/media` go to Django on port 8000.

```bash
cd frontend
npm install
npm run dev
```

The app will be at [http://127.0.0.1:5173/].

Keep Django running on port 8000 in another terminal so API and media requests work.

## Running both together

1. Start the backend: `python manage.py runserver` (in `backend/`, venv active).
2. Start the frontend: `npm run dev` (in `frontend/`).
3. Use the site at [http://127.0.0.1:5173/](http://127.0.0.1:5173/).

## Notes

- Metadata lives in PostgreSQL; PNG/SVG files live under `backend/media/` (paths stored on each Icon).
- Do **not** commit `backend/media/` or large icon zips — use the import command instead.
- Frontend calls should use paths like `/api/...` so the Vite proxy can forward them to Django.
