from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from .models import Expense, ExpenseIn, TotalsResponse, CategoryTotal
from .storage import ExpenseStore

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A small REST API for tracking personal expenses.",
    version="1.0.0",
)

store = ExpenseStore()


@app.get("/", tags=["meta"])
def root():
    return {"message": "Smart Expense Tracker API. See /docs for OpenAPI UI."}


@app.post("/expenses", response_model=Expense, status_code=201, tags=["expenses"])
def add_expense(expense: ExpenseIn):
    """Add a new expense."""
    return store.add(expense)


@app.get("/expenses", response_model=list[Expense], tags=["expenses"])
def list_expenses(category: str | None = Query(default=None, description="Filter by category")):
    """List all expenses, optionally filtered by category."""
    return store.list_all(category=category)


@app.get("/expenses/total", response_model=TotalsResponse, tags=["expenses"])
def get_totals():
    """Overall total and per-category totals."""
    overall, by_cat = store.totals()
    return TotalsResponse(
        overall_total=overall,
        by_category=[CategoryTotal(category=k, total=v) for k, v in by_cat.items()],
    )


@app.get("/expenses/search", response_model=list[Expense], tags=["expenses"])
def search_expenses(q: str = Query(..., min_length=1, description="Search title or category")):
    """Bonus: search expenses by title or category (case-insensitive substring match)."""
    return store.search(q)


@app.get("/expenses/{expense_id}", response_model=Expense, tags=["expenses"])
def get_expense(expense_id: int):
    expense = store.get(expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")
    return expense


@app.delete("/expenses/{expense_id}", status_code=204, tags=["expenses"])
def delete_expense(expense_id: int):
    """Delete an expense by id."""
    deleted = store.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")
    return JSONResponse(status_code=204, content=None)
