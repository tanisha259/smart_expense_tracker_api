# Smart Expense Tracker API

A small REST API for tracking personal expenses, built with **FastAPI** and
**Python**. Data is stored as JSON on disk (`data/expenses.json`), loaded into
memory on startup — no database required.

## Features

- `POST /expenses` — add an expense (`title`, `amount`, `category`, `date`)
- `GET /expenses` — list all expenses (optionally `?category=Food`)
- `GET /expenses/{id}` — get a single expense
- `GET /expenses/total` — overall total and totals broken down by category
- `DELETE /expenses/{id}` — delete an expense
- `GET /expenses/search?q=` — **bonus**: search by title or category (case-insensitive substring match)
- Interactive OpenAPI/Swagger docs at `/docs` (free from FastAPI)

## Requirements

- Python 3.10+

## Install

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn src.main:app --reload
```

The API is now available at `http://127.0.0.1:8000`.
Swagger UI: `http://127.0.0.1:8000/docs`

## Run the tests

```bash
python -m pytest tests/ -v
```

Tests use FastAPI's `TestClient` and clear the store before/after each test,
so they don't depend on or pollute `data/expenses.json`.

## Example requests

```bash
# Add an expense
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Coffee", "amount": 4.50, "category": "Food", "date": "2026-07-01"}'

# List all
curl http://127.0.0.1:8000/expenses

# Filter by category
curl "http://127.0.0.1:8000/expenses?category=Food"

# Totals
curl http://127.0.0.1:8000/expenses/total

# Search
curl "http://127.0.0.1:8000/expenses/search?q=coffee"

# Delete
curl -X DELETE http://127.0.0.1:8000/expenses/1
```

## Project structure

```
your-repo/
  README.md
  AI_NOTES.md
  requirements.txt
  src/
    __init__.py
    main.py        # FastAPI app and route handlers
    models.py       # Pydantic request/response models + validation
    storage.py       # JSON-file-backed in-memory store
  tests/
    test_api.py     # pytest suite covering all endpoints
  data/
    expenses.json   # created automatically at runtime (gitignored)
```

## Design notes

- **Validation**: `amount` must be a positive number; `title`/`category`
  can't be blank. Invalid input returns `422` with details from Pydantic.
- **Persistence**: every write (add/delete) is flushed to
  `data/expenses.json` immediately, so restarting the server preserves data.
- **Category filtering/search** are case-insensitive.
- **Deleting** a non-existent id returns `404`.
