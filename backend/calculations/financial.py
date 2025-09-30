"""
Core financial calculation functions for real estate analysis.

Formulas from INITIAL.md:
- GMI (Gross Monthly Income) = Monthly Rent (legal or market) + Other Property Income
- VCL (Vacancy & Credit Loss) = GMI × Vacancy Rate
- OE (Operating Expenses) = Sum of recurring non-debt costs
- NOI (Net Operating Income) = (GMI − VCL) × 12 − Annual OE
- ADS (Annual Debt Service) = 12 × Monthly Mortgage Payment
- DSCR (Debt Service Coverage Ratio) = NOI ÷ ADS
- TMC (Total Monthly Cost) = Principal + Interest + Monthly OE + Insurance + Management Fees − Monthly Tax Effects
- Cap Rate = NOI ÷ Purchase Price
- CoC (Cash-on-Cash Return) = Annual Pre-Tax Cash Flow ÷ Initial Cash Invested
- Price-to-Rent (Years) = Purchase Price ÷ Annual Rent
- LTV (Loan-to-Value) = Loan Amount ÷ Purchase Price
"""


def gross_monthly_income(monthly_rent: float, other_income: float = 0.0) -> float:
    """
    Calculate Gross Monthly Income (GMI).

    Args:
        monthly_rent: Monthly rental income
        other_income: Other property income (parking, storage, etc.)

    Returns:
        float: Gross monthly income

    Formula:
        GMI = Monthly Rent + Other Property Income
    """
    return monthly_rent + other_income


def vacancy_credit_loss(gmi: float, vacancy_rate: float) -> float:
    """
    Calculate Vacancy & Credit Loss (VCL).

    Args:
        gmi: Gross monthly income
        vacancy_rate: Vacancy rate (e.g., 0.05 for 5%)

    Returns:
        float: Vacancy and credit loss amount

    Formula:
        VCL = GMI × Vacancy Rate
    """
    return gmi * vacancy_rate


def noi_calculation(
    gmi: float,
    vcl: float,
    annual_operating_expenses: float
) -> float:
    """
    Calculate Net Operating Income (NOI).

    Args:
        gmi: Gross monthly income
        vcl: Vacancy & credit loss (monthly)
        annual_operating_expenses: Annual operating expenses

    Returns:
        float: Net operating income (annual)

    Formula:
        NOI = (GMI − VCL) × 12 − Annual OE
    """
    return (gmi - vcl) * 12 - annual_operating_expenses


def annual_debt_service(monthly_mortgage_payment: float) -> float:
    """
    Calculate Annual Debt Service (ADS).

    Args:
        monthly_mortgage_payment: Monthly mortgage payment

    Returns:
        float: Annual debt service

    Formula:
        ADS = 12 × Monthly Mortgage Payment
    """
    return monthly_mortgage_payment * 12


def dscr_calculation(noi: float, ads: float) -> float:
    """
    Calculate Debt Service Coverage Ratio (DSCR).

    Args:
        noi: Net operating income (annual)
        ads: Annual debt service

    Returns:
        float: DSCR (must be > 1.0 for positive cash flow)

    Formula:
        DSCR = NOI ÷ ADS

    Note:
        DSCR < 1.0 means property loses money (negative cash flow)
        DSCR = 1.0 means break-even
        DSCR > 1.0 means positive cash flow
    """
    if ads == 0:
        return float('inf') if noi > 0 else 0.0
    return noi / ads


def cap_rate(noi: float, purchase_price: float) -> float:
    """
    Calculate Capitalization Rate (Cap Rate).

    Args:
        noi: Net operating income (annual)
        purchase_price: Property purchase price

    Returns:
        float: Cap rate as a decimal (e.g., 0.05 for 5%)

    Formula:
        Cap Rate = NOI ÷ Purchase Price
    """
    if purchase_price == 0:
        return 0.0
    return noi / purchase_price


def cash_on_cash(annual_pre_tax_cash_flow: float, initial_cash_invested: float) -> float:
    """
    Calculate Cash-on-Cash Return (CoC).

    Args:
        annual_pre_tax_cash_flow: Annual pre-tax cash flow
        initial_cash_invested: Initial cash invested (down payment + closing costs)

    Returns:
        float: CoC return as a decimal (e.g., 0.08 for 8%)

    Formula:
        CoC = Annual Pre-Tax Cash Flow ÷ Initial Cash Invested
        where Annual Pre-Tax Cash Flow = (GMI − VCL − Monthly OE − Monthly Debt Service) × 12
    """
    if initial_cash_invested == 0:
        return 0.0
    return annual_pre_tax_cash_flow / initial_cash_invested


def price_to_rent_ratio(purchase_price: float, annual_rent: float) -> float:
    """
    Calculate Price-to-Rent ratio in years.

    Args:
        purchase_price: Property purchase price
        annual_rent: Annual rental income

    Returns:
        float: Number of years to recover purchase price through rent

    Formula:
        Price-to-Rent = Purchase Price ÷ Annual Rent
    """
    if annual_rent == 0:
        return float('inf')
    return purchase_price / annual_rent


def ltv_ratio(loan_amount: float, purchase_price: float) -> float:
    """
    Calculate Loan-to-Value ratio (LTV).

    Args:
        loan_amount: Loan amount
        purchase_price: Property purchase price

    Returns:
        float: LTV as a decimal (e.g., 0.80 for 80%)

    Formula:
        LTV = Loan Amount ÷ Purchase Price
    """
    if purchase_price == 0:
        return 0.0
    return loan_amount / purchase_price


def total_monthly_cost(
    principal_payment: float,
    interest_payment: float,
    monthly_operating_expenses: float,
    monthly_tax_benefit: float = 0.0
) -> float:
    """
    Calculate Total Monthly Cost (TMC).

    Args:
        principal_payment: Monthly principal payment
        interest_payment: Monthly interest payment
        monthly_operating_expenses: Monthly operating expenses
        monthly_tax_benefit: Monthly tax benefit (deductions)

    Returns:
        float: Total monthly cost

    Formula:
        TMC = Principal + Interest + Monthly OE + Insurance + Management − Monthly Tax Effects
    """
    return (principal_payment + interest_payment +
            monthly_operating_expenses - monthly_tax_benefit)