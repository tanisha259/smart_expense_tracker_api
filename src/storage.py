"""Simple JSON-file-backed storage for expenses.

Data is kept in memory (a dict keyed by id) for fast access and
persisted to disk on every write so it survives restarts.
"""
import json
from pathlib import Path
from threading import Lock
from typing import Optional

from .models import Expense, ExpenseIn

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "expenses.json"


class ExpenseStore:
    def __init__(self, data_file: Path = DATA_FILE):
        self._data_file = data_file
        self._lock = Lock()
        self._expenses: dict[int, Expense] = {}
        self._next_id = 1
        self._load()

    def _load(self) -> None:
        self._data_file.parent.mkdir(parents=True, exist_ok=True)
        if self._data_file.exists():
            raw = json.loads(self._data_file.read_text() or "[]")
            for item in raw:
                exp = Expense(**item)
                self._expenses[exp.id] = exp
            if self._expenses:
                self._next_id = max(self._expenses.keys()) + 1

    def _persist(self) -> None:
        payload = [json.loads(e.model_dump_json()) for e in self._expenses.values()]
        self._data_file.write_text(json.dumps(payload, indent=2, default=str))

    def add(self, data: ExpenseIn) -> Expense:
        with self._lock:
            expense = Expense(id=self._next_id, **data.model_dump())
            self._expenses[expense.id] = expense
            self._next_id += 1
            self._persist()
            return expense

    def list_all(self, category: Optional[str] = None) -> list[Expense]:
        items = list(self._expenses.values())
        if category:
            items = [e for e in items if e.category.lower() == category.lower()]
        return sorted(items, key=lambda e: e.date, reverse=True)

    def search(self, q: str) -> list[Expense]:
        q_lower = q.lower()
        return [
            e for e in self._expenses.values()
            if q_lower in e.title.lower() or q_lower in e.category.lower()
        ]

    def get(self, expense_id: int) -> Optional[Expense]:
        return self._expenses.get(expense_id)

    def delete(self, expense_id: int) -> bool:
        with self._lock:
            if expense_id in self._expenses:
                del self._expenses[expense_id]
                self._persist()
                return True
            return False

    def totals(self) -> tuple[float, dict[str, float]]:
        overall = 0.0
        by_category: dict[str, float] = {}
        for e in self._expenses.values():
            overall += e.amount
            by_category[e.category] = by_category.get(e.category, 0.0) + e.amount
        return round(overall, 2), {k: round(v, 2) for k, v in by_category.items()}

    def clear(self) -> None:
        """Test helper: wipe all in-memory + on-disk data."""
        with self._lock:
            self._expenses.clear()
            self._next_id = 1
            self._persist()
