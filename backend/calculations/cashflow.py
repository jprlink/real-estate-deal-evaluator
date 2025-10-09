"""
Cash flow projection calculations with property appreciation.

Calculates yearly cash flows including rental income, expenses,
mortgage payments, and property value appreciation.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class CashFlowProjection:
    """
    Detailed cash flow projection for a single year.

    Attributes:
        year: Year number (1-indexed)
        rental_income: Annual rental income
        operating_expenses: Operating expenses (property tax, insurance, maintenance, HOA)
        mortgage_payment: Annual mortgage payment (principal + interest)
        noi: Net Operating Income (rental_income - operating_expenses)
        cash_flow: Annual cash flow after mortgage (noi - mortgage_payment)
        cumulative_cash_flow: Cumulative cash flow from year 1 to current year
        property_value: Estimated property value at end of year
        equity: Equity in property (property_value - remaining_loan_balance)
        remaining_loan_balance: Remaining loan balance at end of year
    """
    year: int
    rental_income: float
    operating_expenses: float
    mortgage_payment: float
    noi: float
    cash_flow: float
    cumulative_cash_flow: float
    property_value: float
    equity: float
    remaining_loan_balance: float


def calculate_cash_flow_projection(
    initial_property_value: float,
    monthly_rent: float,
    monthly_operating_expenses: float,
    monthly_mortgage_payment: float,
    loan_amortization_schedule: List[Dict[str, float]],
    appreciation_rate: float,
    years: int = 10
) -> List[CashFlowProjection]:
    """
    Calculate detailed cash flow projections over multiple years.

    Args:
        initial_property_value: Initial property purchase price
        monthly_rent: Monthly rental income
        monthly_operating_expenses: Monthly operating expenses (tax, insurance, maintenance, HOA)
        monthly_mortgage_payment: Monthly mortgage payment
        loan_amortization_schedule: List of payment details from mortgage.amortization_schedule()
                                   Each dict contains: {payment, principal, interest, balance}
        appreciation_rate: Annual property appreciation rate as decimal (e.g., 0.03 for 3%)
        years: Number of years to project (default: 10)

    Returns:
        List[CashFlowProjection]: Yearly cash flow projections

    Example:
        >>> schedule = amortization_schedule(400000, 0.035, 20)
        >>> projections = calculate_cash_flow_projection(
        ...     initial_property_value=500000,
        ...     monthly_rent=2500,
        ...     monthly_operating_expenses=600,
        ...     monthly_mortgage_payment=2317.30,
        ...     loan_amortization_schedule=schedule,
        ...     appreciation_rate=0.02,  # 2% per year
        ...     years=10
        ... )
    """
    projections: List[CashFlowProjection] = []
    cumulative_cf = 0.0
    current_property_value = initial_property_value

    for year in range(1, years + 1):
        # Annual values
        annual_rent = monthly_rent * 12
        annual_opex = monthly_operating_expenses * 12

        # Remaining loan balance (get balance at end of year from amortization schedule)
        # Amortization schedule is monthly, so year N corresponds to month N*12
        month_index = year * 12 - 1  # 0-indexed
        if month_index < len(loan_amortization_schedule):
            remaining_balance = loan_amortization_schedule[month_index]["remaining_balance"]
            # Mortgage payment only applies while loan exists
            annual_mortgage = monthly_mortgage_payment * 12
        else:
            # Loan paid off - no more mortgage payments!
            remaining_balance = 0.0
            annual_mortgage = 0.0

        # NOI
        noi = annual_rent - annual_opex

        # Cash flow (after mortgage is paid off, cash flow = NOI)
        cash_flow = noi - annual_mortgage
        cumulative_cf += cash_flow

        # Property appreciation
        current_property_value *= (1 + appreciation_rate)

        # Equity
        equity = current_property_value - remaining_balance

        projection = CashFlowProjection(
            year=year,
            rental_income=annual_rent,
            operating_expenses=annual_opex,
            mortgage_payment=annual_mortgage,
            noi=noi,
            cash_flow=cash_flow,
            cumulative_cash_flow=cumulative_cf,
            property_value=current_property_value,
            equity=equity,
            remaining_loan_balance=remaining_balance
        )

        projections.append(projection)

    return projections


def calculate_total_return_with_sale(
    projections: List[CashFlowProjection],
    initial_equity: float,
    selling_costs_rate: float = 0.08
) -> Dict[str, float]:
    """
    Calculate total return including property sale at final year.

    Args:
        projections: List of cash flow projections from calculate_cash_flow_projection()
        initial_equity: Initial equity invested (down payment + closing costs)
        selling_costs_rate: Selling costs as % of sale price (default: 8% in France)

    Returns:
        dict: {
            "final_property_value": Property value at sale,
            "selling_costs": Estimated selling costs,
            "remaining_loan_balance": Loan balance to pay off,
            "net_sale_proceeds": Net proceeds from sale,
            "total_cash_flows": Sum of all annual cash flows,
            "total_return": Total return (cash flows + net proceeds),
            "total_return_on_equity": Total return / initial equity
        }
    """
    if not projections:
        return {
            "final_property_value": 0.0,
            "selling_costs": 0.0,
            "remaining_loan_balance": 0.0,
            "net_sale_proceeds": 0.0,
            "total_cash_flows": 0.0,
            "total_return": 0.0,
            "total_return_on_equity": 0.0
        }

    final_projection = projections[-1]

    final_value = final_projection.property_value
    selling_costs = final_value * selling_costs_rate
    remaining_balance = final_projection.remaining_loan_balance
    net_proceeds = final_value - selling_costs - remaining_balance

    total_cfs = sum(p.cash_flow for p in projections)
    total_return = total_cfs + net_proceeds

    return_on_equity = total_return / initial_equity if initial_equity > 0 else 0.0

    return {
        "final_property_value": final_value,
        "selling_costs": selling_costs,
        "remaining_loan_balance": remaining_balance,
        "net_sale_proceeds": net_proceeds,
        "total_cash_flows": total_cfs,
        "total_return": total_return,
        "total_return_on_equity": return_on_equity
    }
