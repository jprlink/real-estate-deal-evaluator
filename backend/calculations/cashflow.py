"""
Cash flow projection calculations with property appreciation.

Calculates yearly cash flows including rental income, expenses,
mortgage payments, and property value appreciation.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


def calculate_french_purchase_costs(purchase_price: float, has_mortgage: bool = True) -> Dict[str, float]:
    """
    Calculate detailed French property purchase costs (frais de notaire).

    Args:
        purchase_price: Property purchase price (excluding renovations)
        has_mortgage: Whether buyer is taking a mortgage

    Returns:
        Dict with breakdown of all costs:
        - registration_duties: Droits d'enregistrement (transfer taxes)
        - notaire_fees: Actual notaire professional fees (émoluments)
        - disbursements: Administrative costs and documentation
        - mortgage_fees: Additional fees if mortgage (optional)
        - total: Total acquisition costs

    Note:
        For resale/old properties: ~7-8% of purchase price
        For new properties: ~2-3% of purchase price
        This calculation is for resale properties.
    """
    # 1. Registration duties (droits d'enregistrement) - varies by department
    # Most departments: 5.80%, some: 5.09%
    # Using 5.80% as the standard rate
    registration_duties = purchase_price * 0.0580

    # 2. Notaire professional fees (émoluments) - sliding scale
    # Rates per bracket (2025):
    # €0-€6,500: 3.945%
    # €6,500-€17,000: 1.627%
    # €17,000-€60,000: 1.085%
    # Over €60,000: 0.814%

    notaire_fees = 0.0
    if purchase_price <= 6500:
        notaire_fees = purchase_price * 0.03945
    elif purchase_price <= 17000:
        notaire_fees = 6500 * 0.03945 + (purchase_price - 6500) * 0.01627
    elif purchase_price <= 60000:
        notaire_fees = 6500 * 0.03945 + (17000 - 6500) * 0.01627 + (purchase_price - 17000) * 0.01085
    else:
        notaire_fees = (6500 * 0.03945 +
                       (17000 - 6500) * 0.01627 +
                       (60000 - 17000) * 0.01085 +
                       (purchase_price - 60000) * 0.00814)

    # 3. Disbursements (frais administratifs)
    # Approximately 0.4% of purchase price for documents, registrations, etc.
    disbursements = purchase_price * 0.004

    # 4. Mortgage-related fees (if applicable)
    # Additional ~0.3-0.5% if mortgage is involved
    mortgage_fees = 0.0
    if has_mortgage:
        mortgage_fees = purchase_price * 0.004  # Conservative 0.4%

    # Total
    total = registration_duties + notaire_fees + disbursements + mortgage_fees

    return {
        "registration_duties": registration_duties,
        "notaire_fees": notaire_fees,
        "disbursements": disbursements,
        "mortgage_fees": mortgage_fees,
        "total": total
    }


@dataclass
class CashFlowProjection:
    """
    Detailed cash flow projection for a single year.

    Attributes:
        year: Year number (1-indexed)
        rental_income: Annual gross rental income (before vacancy)
        vacancy_loss: Annual vacancy & credit loss (rental_income * vacancy_rate)
        effective_rental_income: Annual rental income after vacancy
        operating_expenses: Operating expenses (property tax, insurance, maintenance, HOA)
        mortgage_payment: Annual mortgage payment (principal + interest)
        noi: Net Operating Income (effective_rental_income - operating_expenses)
        cash_flow: Annual cash flow after mortgage (noi - mortgage_payment)
        cumulative_cash_flow: Cumulative cash flow from year 1 to current year
        property_value: Estimated property value at end of year
        equity: Equity in property (property_value - remaining_loan_balance)
        remaining_loan_balance: Remaining loan balance at end of year
    """
    year: int
    rental_income: float
    vacancy_loss: float
    effective_rental_income: float
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
    vacancy_rate: float = 0.05,
    years: int = 10,
    down_payment: float = 0,
    renovation_costs: float = 0,
    purchase_fees: float = 0
) -> List[CashFlowProjection]:
    """
    Calculate detailed cash flow projections over multiple years.

    Args:
        initial_property_value: Initial property purchase price
        monthly_rent: Monthly rental income (gross)
        monthly_operating_expenses: Monthly operating expenses (tax, insurance, maintenance, HOA)
        monthly_mortgage_payment: Monthly mortgage payment
        loan_amortization_schedule: List of payment details from mortgage.amortization_schedule()
                                   Each dict contains: {payment, principal, interest, balance}
        appreciation_rate: Annual property appreciation rate as decimal (e.g., 0.03 for 3%)
        vacancy_rate: Vacancy & credit loss rate as decimal (default: 0.05 for 5%)
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
        ...     vacancy_rate=0.05,  # 5% vacancy
        ...     years=10
        ... )
    """
    projections: List[CashFlowProjection] = []
    cumulative_cf = 0.0
    current_property_value = initial_property_value

    # Add Year 0: Purchase costs
    # Total cash required = down payment + renovation costs + all purchase fees
    year_0_cash_out = -(down_payment + renovation_costs + purchase_fees)

    # Initial loan balance (if any)
    initial_loan_balance = loan_amortization_schedule[0]["remaining_balance"] if loan_amortization_schedule else 0

    # Initial equity = property value (after renovation) - loan balance
    # Note: Purchase fees are COSTS that disappear, not equity
    initial_equity = initial_property_value - initial_loan_balance

    year_0 = CashFlowProjection(
        year=0,
        rental_income=0,  # No rent in year 0
        vacancy_loss=0,
        effective_rental_income=0,
        operating_expenses=0,
        mortgage_payment=0,
        noi=0,
        cash_flow=year_0_cash_out,  # Negative cash flow (money out)
        cumulative_cash_flow=year_0_cash_out,
        property_value=initial_property_value,  # Property value after purchase + renovation
        equity=initial_equity,  # Correct equity: property value - loan
        remaining_loan_balance=initial_loan_balance
    )
    projections.append(year_0)
    cumulative_cf = year_0_cash_out

    for year in range(1, years + 1):
        # Annual values
        annual_rent = monthly_rent * 12
        annual_vacancy_loss = annual_rent * vacancy_rate
        effective_annual_rent = annual_rent - annual_vacancy_loss
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

        # NOI (using effective rental income after vacancy)
        noi = effective_annual_rent - annual_opex

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
            vacancy_loss=annual_vacancy_loss,
            effective_rental_income=effective_annual_rent,
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
