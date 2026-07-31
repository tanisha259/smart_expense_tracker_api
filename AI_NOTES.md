# AI Integration & Development Notes

This document outlines my process for building the Smart Expense Tracker API, specifically detailing how I leveraged AI tools to accelerate boilerplate generation while maintaining strict architectural ownership, code quality, and alignment with the project requirements.

## 1. AI-Generated vs. Human-Written Code

*   **AI-Generated (Scaffolding & Boilerplate):** 
    *   Initial FastAPI routing definitions (`src/main.py`).
    *   Base Pydantic schema structures for request/response serialization (`src/models.py`).
    *   The foundational synchronous file read/write logic for JSON persistence (`src/storage.py`).
    *   First-pass test cases for basic CRUD operations (`tests/test_api.py`).
*   **Written & Heavily Modified by Me (Business Logic & Edge Cases):**
    *   **Case-Insensitive Filtering:** The AI initially implemented exact-match filtering. I completely rewrote the filtering logic in `src/storage.py` and the corresponding tests to be case-insensitive, recognizing that a strict match creates friction for the end user.
    *   **Search Feature (Bonus Requirement):** I independently designed and implemented the `/expenses/search` endpoint. I ensured it performs robust substring matching across both `title` and `category` fields to provide maximum utility.
    *   **Strict Data Validation:** The AI's initial Pydantic schema failed to validate negative numbers. I manually enforced strict constraints (e.g., `amount > 0`, non-empty strings) using Pydantic's `Field` validations to ensure absolute data integrity.
    *   **RESTful Best Practices:** I refactored the `DELETE` endpoint to return a `204 No Content` status code, correcting the AI's generation of a `200 OK` response with a JSON payload, thereby adhering strictly to REST standards.

## 2. Validation, Testing, and Quality Assurance

I treated the AI's output as an initial draft rather than production-ready code. My validation process included:
*   **Automated Testing:** I expanded the AI-generated pytest suite to ensure comprehensive coverage of edge cases, particularly focusing on the constraints I added (e.g., rejecting blank titles and negative amounts).
*   **Manual Endpoint Verification:** I rigorously tested all endpoints using `curl` and the provided Swagger UI (`/docs`), ensuring the API contract was exactly as specified in the project requirements.
*   **Data Persistence Verification:** I manually verified that data was flushed to `data/expenses.json` immediately upon mutation, guaranteeing that data survives server restarts without corruption or data loss.

## 3. AI Suggestions Rejected & Architectural Decisions

To ensure the codebase remained clean, maintainable, and strictly within the scope of the requirements, I actively rejected several AI proposals:
*   **Rejected SQLite Integration:** The AI strongly suggested migrating from JSON to a SQLite database. **Why:** The project brief explicitly stated "no database required." Introducing SQL would violate the constraints, introduce unnecessary dependencies, and overcomplicate the architecture for a simple in-memory tracking tool. 
*   **Rejected Asynchronous I/O (aiofiles):** The AI proposed using `aiofiles` to make file reading/writing asynchronous. **Why:** For an application with a single-user profile where data is loaded into memory on startup and synced to a local file, async file I/O introduces unwarranted complexity without tangible performance benefits. I opted for synchronous operations to prioritize code readability and simplicity.
*   **Rejected Complex ORMs:** The AI attempted to introduce SQLAlchemy schemas. **Why:** I stripped this out immediately to rely purely on Pydantic and native Python dictionaries, keeping the footprint minimal and the application fast.

## Tools Leveraged
*   **Claude 3.5 Sonnet:** For initial rapid prototyping and structural scaffolding.
*   **GitHub Copilot:** For inline auto-completion and test case generation.
