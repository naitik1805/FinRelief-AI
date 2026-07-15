"""
Financial Engine Module
------------------------
Calculates real-time financial health metrics including EMI-to-income ratio,
debt-to-income ratio, monthly surplus, total outstanding debt, and financial
stress level based on the borrower's income, expenses, and loan portfolio.
"""

from typing import List


def calculate_financial_health(user, loans: List) -> dict:
    """Calculate financial health metrics for a borrower."""
    total_emi = sum(loan.emi for loan in loans)
    total_outstanding = sum(loan.outstanding_amount for loan in loans)
    surplus = user.monthly_income - user.monthly_expenses - total_emi

    # EMI Ratio = (total_emi / monthly_income) * 100
    if user.monthly_income > 0:
        emi_ratio = (total_emi / user.monthly_income) * 100
    else:
        emi_ratio = 0

    # Debt-to-Income = (total_outstanding / monthly_income) * 100
    if user.monthly_income > 0:
        debt_to_income = (total_outstanding / user.monthly_income) * 100
    else:
        debt_to_income = 0

    # Stress Level Logic:
    # <30 -> Low
    # 30-50 -> Medium
    # >50 -> High
    if emi_ratio > 50:
        stress_level = "High"
    elif emi_ratio >= 30:
        stress_level = "Medium"
    else:
        stress_level = "Low"

    return {
        "total_emi": total_emi,
        "total_outstanding": total_outstanding,
        "surplus": round(surplus, 2),
        "emi_ratio_percent": round(emi_ratio, 2),
        "debt_to_income_percent": round(debt_to_income, 2),
        "stress_level": stress_level,
        "total_loans": len(loans)
    }


def calculate_loan_priority(loans: List, emi_ratio: float = 0) -> List[dict]:
    """
    Analyzes borrower loan portfolio and assigns priority levels based on
    overdue duration, interest rate, and EMI burden for intelligent debt management.
    """
    priority_list = []

    for loan in loans:
        # Determine priority based on rules
        is_overdue = loan.overdue_months > 0
        high_interest = loan.interest_rate > 12
        high_emi_ratio = emi_ratio > 50

        if is_overdue or high_interest or high_emi_ratio:
            priority = "High"
        elif loan.interest_rate > 8 or loan.overdue_months > 0:
            priority = "Medium"
        else:
            priority = "Low"

        priority_list.append({
            "loan_id": loan.id,
            "lender_name": loan.lender_name,
            "outstanding_amount": loan.outstanding_amount,
            "interest_rate": loan.interest_rate,
            "overdue_months": loan.overdue_months,
            "emi": loan.emi,
            "priority": priority
        })

    # Sort by priority (High first)
    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    priority_list.sort(key=lambda x: priority_order[x["priority"]])

    return priority_list


def simulate_debt_timeline(user, loans: List, extra_payment: float = 0) -> dict:
    """
    Simulates monthly debt repayment progression and balance reduction
    scenarios based on borrower repayment capacity and additional payment
    strategies.
    """
    loan_data = [
        {
            "loan_id": loan.id,
            "balance": loan.outstanding_amount,
            "interest_rate": loan.interest_rate,
            "emi": loan.emi
        }
        for loan in loans
    ]

    months = 0
    max_months = 240
    timeline = []

    while any(loan["balance"] > 0 for loan in loan_data) and months < max_months:
        months += 1
        total_balance = 0

        # Sort loans by financial urgency (highest balance repaid first)
        loan_data.sort(key=lambda x: x["balance"], reverse=True)

        for loan in loan_data:
            if loan["balance"] <= 0:
                continue

            monthly_interest = (loan["interest_rate"] / 100) / 12
            loan["balance"] += loan["balance"] * monthly_interest

            payment = loan["emi"]

            if extra_payment > 0 and loan == loan_data[0]:
                payment += extra_payment

            loan["balance"] -= payment

            if loan["balance"] < 0:
                loan["balance"] = 0

            total_balance += loan["balance"]

        timeline.append({
            "month": months,
            "remaining_balance": round(total_balance, 2)
        })

    return {
        "months_to_debt_free": months,
        "final_remaining_balance": round(total_balance, 2) if loan_data else 0,
        "timeline_preview": timeline[:12]
    }
