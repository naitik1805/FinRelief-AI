"""
AI Negotiation Strategy Engine
-------------------------------
- Analyzes borrower's complete financial profile and loan data
- Generates personalized settlement strategies using Google Gemini API
- Produces lender-specific professional negotiation letters
- Activates rule-based fallback engine when API key is unavailable
"""

import os
import importlib
from datetime import date

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")


def _call_gemini(prompt: str) -> str:
    """Call Google Gemini API if key is available, otherwise use rule-based fallback."""
    if not GOOGLE_API_KEY:
        return None  # Will fall through to fallback

    try:
        genai = importlib.import_module("google.generativeai")
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except ImportError:
        return None
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


# ---------- Negotiation Strategy ----------

def generate_negotiation_strategy(user, loans, financial_health, settlement_data) -> str:
    """Generate an AI (or fallback) negotiation strategy summary across all loans."""

    prompt = f"""
    You are a financial negotiation expert. Based on the following borrower data,
    generate a clear, professional debt negotiation strategy.

    Monthly Income: {user.monthly_income}
    Monthly Expenses: {user.monthly_expenses}
    Financial Stress Level: {financial_health.get('stress_level')}
    EMI Ratio: {financial_health.get('emi_ratio_percent')}%
    Total Outstanding Debt: {financial_health.get('total_outstanding')}

    Loans:
    {[{'lender': s['lender_name'], 'amount': s['outstanding_amount'], 'settlement_percent': s['suggested_settlement_percentage'], 'risk': s['risk_category']} for s in settlement_data]}

    Provide a short negotiation strategy (bullet points) covering:
    1. Which loans to prioritize negotiating first
    2. Suggested settlement approach for each lender
    3. Key talking points for the borrower
    4. Realistic timeline expectations
    """

    ai_response = _call_gemini(prompt)
    if ai_response:
        return ai_response

    # ---------- Rule-based fallback ----------
    lines = ["AI NEGOTIATION STRATEGY (Rule-Based Fallback)", ""]
    lines.append(f"Financial Stress Level: {financial_health.get('stress_level')}")
    lines.append(f"EMI-to-Income Ratio: {financial_health.get('emi_ratio_percent')}%")
    lines.append("")
    lines.append("Recommended Negotiation Order:")

    sorted_data = sorted(settlement_data, key=lambda x: x["risk_score"], reverse=True)
    for idx, s in enumerate(sorted_data, start=1):
        lines.append(
            f"{idx}. {s['lender_name']} — Outstanding: Rs.{s['outstanding_amount']}, "
            f"Suggested Settlement: {s['suggested_settlement_percentage']}% "
            f"(Recommended payoff: Rs.{s['recommended_amount']}), Risk: {s['risk_category']}"
        )

    lines.append("")
    lines.append("Key Talking Points:")
    lines.append("- Highlight genuine financial hardship with supporting documents")
    lines.append("- Propose a one-time lump sum settlement where possible")
    lines.append("- Request written confirmation of settlement terms before payment")
    lines.append("- Ask for a 'No Dues Certificate' after final payment")
    lines.append("")
    lines.append("Suggested Timeline: 30-45 days for negotiating and finalizing settlement per loan.")

    return "\n".join(lines)


# ---------- Negotiation Email / Letter ----------

def generate_negotiation_email(user, loan, financial_health, settlement_info) -> str:
    """Generate a lender-specific negotiation email/settlement letter."""

    prompt = f"""
    Write a professional, polite settlement negotiation email to a lender.

    Lender: {loan.lender_name}
    Loan Account Type: {loan.loan_type}
    Outstanding Amount: {loan.outstanding_amount}
    Overdue Months: {loan.overdue_months}
    Suggested Settlement Percentage: {settlement_info.get('suggested_settlement_percentage')}%
    Recommended Settlement Amount: {settlement_info.get('recommended_amount')}
    Borrower Monthly Income: {user.monthly_income}
    Financial Stress Level: {financial_health.get('stress_level')}

    The email should:
    - Be respectful and professional
    - Explain financial hardship briefly
    - Propose the settlement amount clearly
    - Request written confirmation
    - Include a proper closing
    """

    ai_response = _call_gemini(prompt)
    if ai_response:
        return ai_response

    # ---------- Rule-based fallback template ----------
    today = date.today().strftime("%d-%m-%Y")

    email = f"""Subject: Request for One-Time Settlement — Loan Account with {loan.lender_name}

Date: {today}

Dear {loan.lender_name} Team,

I am writing to formally request a one-time settlement for my outstanding
loan account with your institution.

ACCOUNT DETAILS:
Loan Type: {loan.loan_type}
Outstanding Amount: Rs.{loan.outstanding_amount}
Overdue Period: {loan.overdue_months} month(s)

FINANCIAL SITUATION:
Due to genuine financial hardship, I am currently unable to continue
repayment as per the original schedule. My monthly income and expenses
have significantly impacted my repayment capacity.

SETTLEMENT PROPOSAL:
I would like to propose a one-time settlement amount of
Rs.{settlement_info.get('recommended_amount')} ({settlement_info.get('suggested_settlement_percentage')}% of the outstanding amount)
to close this account fully.

I kindly request:
1. Written confirmation of the settlement terms
2. A "No Dues Certificate" after final payment
3. Update of the loan status with credit bureaus post-settlement

I appreciate your understanding and look forward to resolving this matter
amicably at the earliest.

Thank you for your consideration.

Sincerely,
{user.name or 'Borrower'}
{user.email}
"""
    return email
