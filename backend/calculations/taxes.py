"""
Tax calculation functions for French real estate investment regimes.

Formulas from INITIAL.md:
- LMNP (furnished) micro-BIC: Taxable = Gross Rent × (1 − Abatement%). Tax = Taxable × Marginal Rate
- Location nue (unfurnished) micro-foncier: Taxable = Gross Rent − Flat Abatement. Tax = Taxable × Marginal Rate
- Régime réel: Taxable = Gross Rent − Actual Deductible Expenses − Interest
"""


def lmnp_micro_bic_tax(
    gross_annual_rent: float,
    abatement_rate: float = 0.50,
    marginal_rate: float = 0.30,
    social_charges_rate: float = 0.172
) -> dict:
    """
    Calculate tax for LMNP (Loueur Meublé Non Professionnel) micro-BIC regime.

    Args:
        gross_annual_rent: Gross annual rental income
        abatement_rate: Abatement rate (default 50% = 0.50 for furnished)
        marginal_rate: Marginal income tax rate (e.g., 0.30 for 30%)
        social_charges_rate: Social charges rate (default 17.2% = 0.172)

    Returns:
        dict: Dictionary with taxable_income, income_tax, social_charges, total_tax

    Formula:
        Taxable Income = Gross Rent × (1 − Abatement%)
        Income Tax = Taxable × Marginal Rate
        Social Charges = Taxable × Social Charges Rate
        Total Tax = Income Tax + Social Charges
    """
    taxable_income = gross_annual_rent * (1 - abatement_rate)
    income_tax = taxable_income * marginal_rate
    social_charges = taxable_income * social_charges_rate
    total_tax = income_tax + social_charges

    return {
        "taxable_income": taxable_income,
        "income_tax": income_tax,
        "social_charges": social_charges,
        "total_tax": total_tax
    }


def location_nue_micro_foncier_tax(
    gross_annual_rent: float,
    flat_abatement: float = 0.30,
    marginal_rate: float = 0.30,
    social_charges_rate: float = 0.172
) -> dict:
    """
    Calculate tax for location nue (unfurnished) micro-foncier regime.

    Args:
        gross_annual_rent: Gross annual rental income
        flat_abatement: Flat abatement rate (default 30% = 0.30)
        marginal_rate: Marginal income tax rate
        social_charges_rate: Social charges rate (default 17.2%)

    Returns:
        dict: Dictionary with taxable_income, income_tax, social_charges, total_tax

    Formula:
        Taxable Income = Gross Rent × (1 − Flat Abatement)
        Income Tax = Taxable × Marginal Rate
        Social Charges = Taxable × Social Charges Rate
        Total Tax = Income Tax + Social Charges
    """
    taxable_income = gross_annual_rent * (1 - flat_abatement)
    income_tax = taxable_income * marginal_rate
    social_charges = taxable_income * social_charges_rate
    total_tax = income_tax + social_charges

    return {
        "taxable_income": taxable_income,
        "income_tax": income_tax,
        "social_charges": social_charges,
        "total_tax": total_tax
    }


def regime_reel_tax(
    gross_annual_rent: float,
    deductible_expenses: float,
    interest_payments: float,
    marginal_rate: float = 0.30,
    social_charges_rate: float = 0.172
) -> dict:
    """
    Calculate tax for régime réel (actual expenses).

    Args:
        gross_annual_rent: Gross annual rental income
        deductible_expenses: Actual deductible expenses
        interest_payments: Mortgage interest payments
        marginal_rate: Marginal income tax rate
        social_charges_rate: Social charges rate

    Returns:
        dict: Dictionary with taxable_income, income_tax, social_charges, total_tax

    Formula:
        Taxable Income = Gross Rent − Actual Deductible Expenses − Interest
        Income Tax = Taxable × Marginal Rate
        Social Charges = Taxable × Social Charges Rate
        Total Tax = Income Tax + Social Charges

    Note:
        Taxable income can be negative (deficit foncier), which can be carried forward
    """
    taxable_income = gross_annual_rent - deductible_expenses - interest_payments

    # Tax only applies to positive taxable income
    income_tax = max(0, taxable_income * marginal_rate)
    social_charges = max(0, taxable_income * social_charges_rate)
    total_tax = income_tax + social_charges

    return {
        "taxable_income": taxable_income,
        "income_tax": income_tax,
        "social_charges": social_charges,
        "total_tax": total_tax,
        "deficit": min(0, taxable_income)  # Negative taxable income = deficit
    }


def after_tax_margin(
    pre_tax_monthly_cash_flow: float,
    annual_income_tax: float,
    annual_social_charges: float
) -> float:
    """
    Calculate after-tax monthly margin.

    Args:
        pre_tax_monthly_cash_flow: Pre-tax monthly cash flow
        annual_income_tax: Annual income tax
        annual_social_charges: Annual social charges

    Returns:
        float: After-tax monthly margin

    Formula:
        After-Tax Margin (Monthly) = Pre-Tax Monthly Cash Flow − (Income Tax + Social Charges)/12
    """
    monthly_tax = (annual_income_tax + annual_social_charges) / 12
    return pre_tax_monthly_cash_flow - monthly_tax