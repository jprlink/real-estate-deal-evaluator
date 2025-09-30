"""
IRR and NPV calculation functions.

Formulas from INITIAL.md:
- IRR (Internal Rate of Return) solves: 0 = Σ(CF_t / (1+r)^t)
  where CF_0 = -Initial Equity; CF_T includes net sale proceeds
- NPV (Net Present Value) at discount rate k: NPV = Σ(CF_t / (1+k)^t)
- Sale Proceeds (Net) = Resale Price − Selling Costs − Remaining Loan Balance
"""

from typing import List
import numpy_financial as npf


def irr_calculation(cash_flows: List[float]) -> float:
    """
    Calculate Internal Rate of Return (IRR).

    Args:
        cash_flows: List of cash flows starting with initial investment (negative)
                   [CF_0, CF_1, CF_2, ..., CF_T]
                   CF_0 should be negative (initial equity)
                   CF_T includes net sale proceeds

    Returns:
        float: IRR as a decimal (e.g., 0.12 for 12%)

    Formula:
        IRR solves: 0 = Σ(CF_t / (1+r)^t) for t=0 to T

    Note:
        Uses numpy-financial library.
        Returns NaN if no IRR can be calculated (e.g., all positive or all negative flows)
    """
    if not cash_flows or len(cash_flows) < 2:
        return float('nan')

    try:
        return float(npf.irr(cash_flows))
    except (ValueError, RuntimeError):
        # No IRR exists (e.g., all cash flows same sign)
        return float('nan')


def npv_calculation(cash_flows: List[float], discount_rate: float) -> float:
    """
    Calculate Net Present Value (NPV).

    Args:
        cash_flows: List of cash flows [CF_0, CF_1, CF_2, ..., CF_T]
        discount_rate: Discount rate as a decimal (e.g., 0.10 for 10%)

    Returns:
        float: NPV value

    Formula:
        NPV = Σ(CF_t / (1+k)^t) for t=0 to T
        where k is the discount rate

    Note:
        Uses numpy-financial library.
    """
    if not cash_flows:
        return 0.0

    return float(npf.npv(discount_rate, cash_flows))


def net_sale_proceeds(
    resale_price: float,
    selling_costs_rate: float,
    remaining_loan_balance: float
) -> float:
    """
    Calculate net sale proceeds.

    Args:
        resale_price: Property resale price
        selling_costs_rate: Selling costs as % of price (e.g., 0.08 for 8%)
        remaining_loan_balance: Remaining loan balance at sale

    Returns:
        float: Net sale proceeds

    Formula:
        Sale Proceeds (Net) = Resale Price − Selling Costs − Remaining Loan Balance
    """
    selling_costs = resale_price * selling_costs_rate
    return resale_price - selling_costs - remaining_loan_balance


def equity_multiple(total_cash_received: float, total_equity_invested: float) -> float:
    """
    Calculate equity multiple (leverage ratio).

    Args:
        total_cash_received: Total cash distributions to equity
        total_equity_invested: Total equity invested

    Returns:
        float: Equity multiple

    Formula:
        Equity Multiple = Total Distributions to Equity ÷ Total Equity Invested
    """
    if total_equity_invested == 0:
        return 0.0
    return total_cash_received / total_equity_invested