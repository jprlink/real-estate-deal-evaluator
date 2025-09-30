"""
Mortgage calculation functions.

Formulas from INITIAL.md:
- Monthly Mortgage (amortizing): M = P × (i / (1 - (1 + i)^-n))
  where P=loan principal, i=monthly interest rate, n=months
"""

from typing import List, Dict


def monthly_payment(principal: float, annual_rate: float, years: int) -> float:
    """
    Calculate monthly mortgage payment for an amortizing loan.

    Args:
        principal: Loan principal amount
        annual_rate: Annual interest rate (e.g., 0.03 for 3%)
        years: Loan term in years

    Returns:
        float: Monthly payment amount

    Formula:
        M = P × (i / (1 - (1 + i)^-n))
        where i = monthly rate, n = number of months
    """
    if principal <= 0 or years <= 0:
        return 0.0

    if annual_rate == 0:
        return principal / (years * 12)

    monthly_rate = annual_rate / 12
    num_payments = years * 12

    payment = principal * (monthly_rate / (1 - (1 + monthly_rate) ** -num_payments))
    return payment


def amortization_schedule(
    principal: float,
    annual_rate: float,
    years: int
) -> List[Dict[str, float]]:
    """
    Generate amortization schedule for a loan.

    Args:
        principal: Loan principal amount
        annual_rate: Annual interest rate (e.g., 0.03 for 3%)
        years: Loan term in years

    Returns:
        List of dictionaries with keys: payment_number, payment, principal_payment,
        interest_payment, remaining_balance
    """
    if principal <= 0 or years <= 0:
        return []

    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = monthly_payment(principal, annual_rate, years)

    schedule = []
    remaining_balance = principal

    for month in range(1, num_payments + 1):
        interest_payment = remaining_balance * monthly_rate
        principal_payment = payment - interest_payment
        remaining_balance -= principal_payment

        schedule.append({
            "payment_number": month,
            "payment": payment,
            "principal_payment": principal_payment,
            "interest_payment": interest_payment,
            "remaining_balance": max(0, remaining_balance)
        })

    return schedule