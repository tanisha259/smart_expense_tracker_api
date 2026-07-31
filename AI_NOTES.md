# AI_NOTES.md

## AI Integration & Development Notes

While building the **Smart Expense Tracker API**, I used AI tools to speed up repetitive tasks like creating the initial project structure and boilerplate code. However, I didn't rely on the generated code as-is. I reviewed everything, made several changes, fixed issues, and implemented some features on my own to make sure the project matched the assignment requirements.

## 1. AI-Generated vs. My Contributions

### AI-assisted code

I used AI mainly for generating the initial structure of the project, including:

* Basic FastAPI application setup (`src/main.py`)
* Initial Pydantic models for request and response validation (`src/models.py`)
* Basic JSON file read/write functionality (`src/storage.py`)
* Starter test cases for CRUD operations (`tests/test_api.py`)

### Changes and features implemented by me

After generating the initial code, I modified and improved several parts:

* **Case-insensitive filtering:**
  The generated code only supported exact matches while filtering expenses. I changed the logic so filtering works regardless of letter case, making it more user-friendly.

* **Search endpoint:**
  I implemented the `/expenses/search` endpoint to support substring search across both the **title** and **category** fields. This was added as part of the bonus functionality.

* **Input validation:**
  I improved the validation rules by ensuring:

  * Amount must be greater than 0.
  * Required text fields cannot be empty.
  * Invalid data is rejected before being stored.

* **DELETE endpoint improvements:**
  The generated version returned a `200 OK` response after deleting an expense. I updated it to return **204 No Content**, which follows standard REST API practices.

## 2. Testing and Validation

I didn't assume the AI-generated code was correct. I tested and verified each part before considering it complete.

My testing process included:

* Expanding the pytest test cases to cover validation errors and edge cases.
* Testing every API endpoint using both **Swagger UI** (`/docs`) and **curl**.
* Verifying that all create, update, and delete operations correctly save changes to `data/expenses.json`.
* Checking that data remains available after restarting the application.

These checks helped ensure the API behaved as expected and met the assignment requirements.

## 3. AI Suggestions I Chose Not to Use

During development, AI suggested a few improvements that I intentionally decided not to include.

### SQLite database

AI recommended replacing the JSON file with SQLite.

**Why I didn't use it:**
The assignment specifically mentions that no database is required. Using SQLite would have added unnecessary complexity and gone beyond the project scope.

### Asynchronous file handling

AI also suggested using `aiofiles` for asynchronous file operations.

**Why I didn't use it:**
Since this project stores a small amount of data in a local JSON file, synchronous file operations are simpler and completely sufficient.

### SQLAlchemy ORM

AI suggested using SQLAlchemy models for data management.

**Why I didn't use it:**
A full ORM was unnecessary for this project. Using Pydantic models and JSON storage kept the code simple, lightweight, and easier to understand.

## AI Tools Used

* **Claude 3.5 Sonnet** – Used for generating the initial project structure and boilerplate code.
* **GitHub Copilot** – Used for code suggestions, auto-completion, and generating some initial test cases.

Overall, AI helped speed up development by handling repetitive setup tasks. I reviewed the generated code, made necessary improvements, implemented additional functionality, and tested everything thoroughly to ensure the final solution met the assignment requirements.
