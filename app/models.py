"""
SQLAlchemy ORM models for FinRelief AI.
Tables: users, loans, ai_history
"""

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=True)

    # Authentication fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Financial profile fields
    monthly_income = Column(Float, nullable=False, default=0.0)
    monthly_expenses = Column(Float, nullable=False, default=0.0)
    lump_sum_available = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    loans = relationship("Loan", back_populates="owner", cascade="all, delete-orphan")
    ai_history = relationship("AIHistory", back_populates="owner", cascade="all, delete-orphan")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    lender_name = Column(String(255), nullable=False)
    loan_type = Column(String(100), nullable=False)
    outstanding_amount = Column(Float, nullable=False, default=0.0)
    interest_rate = Column(Float, nullable=False, default=0.0)
    overdue_months = Column(Integer, nullable=False, default=0)
    emi = Column(Float, nullable=False, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="loans")


class AIHistory(Base):
    __tablename__ = "ai_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    query_type = Column(String(100), nullable=False)   # e.g. "Negotiation Strategy", "Negotiation Email"
    response = Column(Text, nullable=False)

    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="ai_history")
