# AI Notes

## What was AI-generated vs. written by me

- **AI-generated**: The initial FastAPI route structure in `src/main.py`, Pydantic validation models in `src/models.py`, the JSON persistence layer in `src/storage.py`, and the first draft of the pytest suite in `tests/test_api.py`.
- **Written/modified by me**: I rewrote the category filtering in `src/storage.py` and the `test_filter_by_category` test to be case-insensitive because the AI's first version did an exact match which made the filtering less user-friendly. I also added the `search` endpoint (the bonus requirement) by carefully incorporating a substring match function on both the title and category fields, and validated `amount` as strictly positive in the Pydantic schema because the AI's initial schema missed checking for negative numbers.

## What I validated, tested, or changed, and why

- Ran the full test suite with `pytest` locally to verify functionality.
- I manually tested each endpoint using `curl` to ensure the responses behaved correctly and matched what's defined in the OpenAPI documentation.
- The AI's first version of the `DELETE /expenses/{id}` endpoint returned a `200 OK` with a JSON payload; I changed it to return a `204 No Content` to adhere more strictly to RESTful conventions.
- Checked that negative amounts and blank titles are rejected by the API—and explicitly verified that Pydantic properly raised `422 Unprocessable Entity` for these inputs.

## AI suggestions I decided not to use, and why

- The AI initially suggested using `SQLite` instead of a JSON file for data storage. I decided against it since the brief explicitly stated no database was required, and a simple JSON file read/write was much simpler to reason about and fully met the requirements for this scope.
- The AI also proposed adding asynchronous file I/O operations (`aiofiles`) for persistence. I judged this to be unnecessary complexity for a single-user local API and kept it synchronous to keep the codebase focused and minimal.

## Tools used

- Claude (web interface), model: Claude 3.5 Sonnet
- GitHub Copilot (in-editor auto-completion)
