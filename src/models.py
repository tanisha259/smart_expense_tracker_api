from datetime import date as date_type
from pydantic import BaseModel, Field, field_validator


class ExpenseIn(BaseModel):
    """Payload for creating an expense. id is server-assigned."""
    title: str = Field(..., min_length=1, max_length=200)
    amount: float = Field(..., gt=0, description="Must be a positive number")
    category: str = Field(..., min_length=1, max_length=100)
    date: date_type

    @field_validator("title", "category")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v


class Expense(ExpenseIn):
    id: int


class CategoryTotal(BaseModel):
    category: str
    total: float


class TotalsResponse(BaseModel):
    overall_total: float
    by_category: list[CategoryTotal]
