"""
FinRelief AI - Main FastAPI Application
Implements all REST API endpoints for authentication, loan management,
financial analysis, settlement prediction, and AI negotiation strategy.
"""

import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app.models import User, Loan, AIHistory
from app.utils.schemas import (
    UserRegister, UserLogin, Token, ProfileUpdate, LoanCreate, LoanResponse
)
from app.utils.auth import (
    hash_password, verify_password, create_access_token, get_current_user
)
from app.services.financial_engine import (
    calculate_financial_health, calculate_loan_priority, simulate_debt_timeline
)
from app.services.settlement_engine import calculate_settlement_probability
from app.services.ai_engine import generate_negotiation_strategy, generate_negotiation_email


# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinRelief AI 🚀",
    description="AI Powered Debt Relief & Financial Recovery Platform",
    version="0.1.0",
)

# Allow the React frontend (Vite dev server locally, or deployed Render URL in production)
# to talk to this API. Set ALLOWED_ORIGINS in .env as a comma-separated list, e.g.
# ALLOWED_ORIGINS=http://localhost:5173,https://finrelief-frontend.onrender.com
_allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = (
    [origin.strip() for origin in _allowed_origins_env.split(",") if origin.strip()]
    if _allowed_origins_env
    else ["*"]  # fallback: allow all origins during local development
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Root / Health check
# ---------------------------------------------------------------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to FinRelief AI 🚀", "status": "running"}


@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"database_status": "Connected ✅"}


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

@app.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user_id": new_user.id}


@app.get("/debug-user")
def debug_user(db: Session = Depends(get_db)):
    """Utility endpoint to check total registered users (used during testing)."""
    count = db.query(User).count()
    return {"total_users": count}


@app.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

@app.put("/update-profile")
def update_profile(
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        user = db.query(User).filter(User.id == current_user.id).first()
        user.monthly_income = profile.monthly_income
        user.monthly_expenses = profile.monthly_expenses
        user.lump_sum_available = profile.lump_sum_available
        db.commit()
        return {"message": "Profile Updated Successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")


# ---------------------------------------------------------------------------
# Loans
# ---------------------------------------------------------------------------

@app.post("/add-loan")
def add_loan(
    loan: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        new_loan = Loan(
            user_id=current_user.id,
            lender_name=loan.lender_name,
            outstanding_amount=loan.outstanding_amount,
            interest_rate=loan.interest_rate,
            overdue_months=loan.overdue_months,
            emi=loan.emi,
            loan_type=loan.loan_type,
        )
        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return {"message": "Loan Added Successfully", "id": new_loan.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to add loan: {str(e)}")


@app.get("/loans", response_model=list[LoanResponse])
def get_loans(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
    return loans


@app.delete("/delete-loan/{loan_id}")
def delete_loan(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loan = db.query(Loan).filter(Loan.id == loan_id, Loan.user_id == current_user.id).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    try:
        db.delete(loan)
        db.commit()
        return {"message": "Loan deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete loan: {str(e)}")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@app.get("/dashboard-data")
def dashboard_data(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
    financial_health = calculate_financial_health(current_user, loans)

    return {
        "name": current_user.name,
        "email": current_user.email,
        "monthly_income": current_user.monthly_income,
        "monthly_expenses": current_user.monthly_expenses,
        "lump_sum_available": current_user.lump_sum_available,
        "financial_health": financial_health,
        "loans": [
            {
                "id": l.id,
                "lender_name": l.lender_name,
                "loan_type": l.loan_type,
                "outstanding_amount": l.outstanding_amount,
                "interest_rate": l.interest_rate,
                "overdue_months": l.overdue_months,
                "emi": l.emi,
            }
            for l in loans
        ],
    }


# ---------------------------------------------------------------------------
# Financial Health / Debt Timeline
# ---------------------------------------------------------------------------

@app.get("/financial-health")
def financial_health(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
    return calculate_financial_health(current_user, loans)


@app.get("/debt-timeline")
def debt_timeline(
    extra_payment: float = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
    if not loans:
        return {"message": "Please add at least one loan to simulate a debt timeline."}
    return simulate_debt_timeline(current_user, loans, extra_payment)


# ---------------------------------------------------------------------------
# Settlement Predictor
# ---------------------------------------------------------------------------

@app.get("/settlement-predictor")
def settlement_predictor(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
    if not loans:
        return {"message": "Please add at least one loan to generate settlement predictions."}

    priority = calculate_loan_priority(loans)
    priority_lookup = {p["loan_id"]: p["priority"] for p in priority}

    settlement_data = calculate_settlement_probability(current_user, loans)
    for s in settlement_data:
        s["priority"] = priority_lookup.get(s["loan_id"], "Low")

    return {"settlements": settlement_data}


# ---------------------------------------------------------------------------
# AI Negotiation Strategy & Email Generation
# ---------------------------------------------------------------------------

@app.get("/ai-negotiation-strategy")
def get_ai_negotiation_strategy(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    try:
        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        if not loans:
            return {"strategy": "Please add at least one loan to generate an AI strategy."}

        financial_health = calculate_financial_health(current_user, loans)
        settlement_data = calculate_settlement_probability(current_user, loans)
        strategy = generate_negotiation_strategy(current_user, loans, financial_health, settlement_data)

        try:
            db.add(AIHistory(user_id=current_user.id, query_type="Negotiation Strategy", response=strategy))
            db.commit()
        except Exception:
            db.rollback()

        return {"strategy": strategy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Strategy error: {str(e)}")


@app.get("/generate-negotiation-email/{loan_id}")
def get_negotiation_email(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        loan = db.query(Loan).filter(Loan.id == loan_id, Loan.user_id == current_user.id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")

        loans = db.query(Loan).filter(Loan.user_id == current_user.id).all()
        financial_health = calculate_financial_health(current_user, loans)
        settlement_data = calculate_settlement_probability(current_user, [loan])[0]

        email_content = generate_negotiation_email(current_user, loan, financial_health, settlement_data)

        try:
            db.add(AIHistory(user_id=current_user.id, query_type="Negotiation Email", response=email_content))
            db.commit()
        except Exception:
            db.rollback()

        return {"email": email_content}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Negotiation email error: {str(e)}")


# ---------------------------------------------------------------------------
# AI History
# ---------------------------------------------------------------------------

@app.get("/ai-history")
def get_ai_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    history = (
        db.query(AIHistory)
        .filter(AIHistory.user_id == current_user.id)
        .order_by(AIHistory.generated_at.desc())
        .all()
    )
    return [
        {
            "id": h.id,
            "query_type": h.query_type,
            "response": h.response,
            "generated_at": h.generated_at,
        }
        for h in history
    ]
