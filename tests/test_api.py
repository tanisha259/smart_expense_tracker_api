import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from fastapi.testclient import TestClient

from src.main import app, store


@pytest.fixture(autouse=True)
def clean_store():
    """Ensure every test starts with an empty store."""
    store.clear()
    yield
    store.clear()


client = TestClient(app)


def make_expense(**overrides):
    payload = {
        "title": "Coffee",
        "amount": 4.50,
        "category": "Food",
        "date": "2026-07-01",
    }
    payload.update(overrides)
    return payload


def test_add_expense():
    resp = client.post("/expenses", json=make_expense())
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Coffee"
    assert body["amount"] == 4.50
    assert body["category"] == "Food"
    assert "id" in body


def test_add_expense_rejects_negative_amount():
    resp = client.post("/expenses", json=make_expense(amount=-5))
    assert resp.status_code == 422


def test_add_expense_rejects_blank_title():
    resp = client.post("/expenses", json=make_expense(title="   "))
    assert resp.status_code == 422


def test_list_expenses_empty():
    resp = client.get("/expenses")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_expenses_returns_added_items():
    client.post("/expenses", json=make_expense(title="Coffee"))
    client.post("/expenses", json=make_expense(title="Bus ticket", category="Transport"))
    resp = client.get("/expenses")
    assert resp.status_code == 200
    titles = {e["title"] for e in resp.json()}
    assert titles == {"Coffee", "Bus ticket"}


def test_filter_by_category():
    client.post("/expenses", json=make_expense(title="Coffee", category="Food"))
    client.post("/expenses", json=make_expense(title="Bus ticket", category="Transport"))
    client.post("/expenses", json=make_expense(title="Lunch", category="food"))  # case-insensitive

    resp = client.get("/expenses", params={"category": "Food"})
    assert resp.status_code == 200
    titles = {e["title"] for e in resp.json()}
    assert titles == {"Coffee", "Lunch"}


def test_totals_overall_and_by_category():
    client.post("/expenses", json=make_expense(title="Coffee", amount=4.5, category="Food"))
    client.post("/expenses", json=make_expense(title="Lunch", amount=10.5, category="Food"))
    client.post("/expenses", json=make_expense(title="Bus", amount=2.0, category="Transport"))

    resp = client.get("/expenses/total")
    assert resp.status_code == 200
    body = resp.json()
    assert body["overall_total"] == 17.0

    by_cat = {c["category"]: c["total"] for c in body["by_category"]}
    assert by_cat == {"Food": 15.0, "Transport": 2.0}


def test_delete_expense():
    created = client.post("/expenses", json=make_expense()).json()
    expense_id = created["id"]

    resp = client.delete(f"/expenses/{expense_id}")
    assert resp.status_code == 204

    resp = client.get(f"/expenses/{expense_id}")
    assert resp.status_code == 404


def test_delete_nonexistent_expense_returns_404():
    resp = client.delete("/expenses/9999")
    assert resp.status_code == 404


def test_get_single_expense():
    created = client.post("/expenses", json=make_expense()).json()
    resp = client.get(f"/expenses/{created['id']}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Coffee"


def test_search_expenses():
    client.post("/expenses", json=make_expense(title="Grocery shopping", category="Food"))
    client.post("/expenses", json=make_expense(title="Bus ticket", category="Transport"))

    resp = client.get("/expenses/search", params={"q": "grocery"})
    assert resp.status_code == 200
    titles = [e["title"] for e in resp.json()]
    assert titles == ["Grocery shopping"]
