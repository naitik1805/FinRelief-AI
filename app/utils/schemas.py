"""
Pydantic schemas used for request validation and response formatting.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# ---------- Auth ----------

class UserRegister(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str = Field(min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Profile ----------

class ProfileUpdate(BaseModel):
    monthly_income: float = Field(ge=0)
    monthly_expenses: float = Field(ge=0)
    lump_sum_available: float = Field(ge=0, default=0.0)


# ---------- Loan ----------

class LoanCreate(BaseModel):
    lender_name: str
    loan_type: str
    outstanding_amount: float = Field(gt=0)
    interest_rate: float = Field(ge=0)
    overdue_months: int = Field(ge=0, default=0)
    emi: float = Field(ge=0)


class LoanResponse(BaseModel):
    id: int
    lender_name: str
    loan_type: str
    outstanding_amount: float
    interest_rate: float
    overdue_months: int
    emi: float

    class Config:
        from_attributes = True
