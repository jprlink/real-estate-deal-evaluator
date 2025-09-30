"""
Financial models for real estate analysis.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class FinancialInputs(BaseModel):
    """User financial inputs for analysis."""
    down_payment: float = Field(..., ge=0, description="Down payment amount (EUR)")
    loan_amount: float = Field(..., ge=0, description="Loan amount (EUR)")
    annual_interest_rate: float = Field(
        ...,
        ge=0,
        le=1,
        description="Annual interest rate (e.g., 0.03 for 3%)"
    )
    loan_term_years: int = Field(..., ge=1, le=30, description="Loan term in years")
    monthly_rent: Optional[float] = Field(None, ge=0, description="Expected monthly rent")
    vacancy_rate: float = Field(
        0.05,
        ge=0,
        le=1,
        description="Vacancy rate (e.g., 0.05 for 5%)"
    )
    operating_expenses_annual: float = Field(
        ...,
        ge=0,
        description="Annual operating expenses (taxes, insurance, maintenance, etc.)"
    )
    holding_period_years: int = Field(
        10,
        ge=1,
        le=30,
        description="Investment holding period in years"
    )
    marginal_tax_rate: float = Field(
        0.30,
        ge=0,
        le=0.50,
        description="Marginal income tax rate"
    )
    rental_regime: str = Field(
        default="location_nue",
        description="Rental regime: location_nue, lmnp, or colocation"
    )
    closing_costs_rate: float = Field(
        0.08,
        ge=0,
        le=0.15,
        description="Closing costs as % of purchase price"
    )
    annual_appreciation_rate: float = Field(
        0.02,
        ge=-0.10,
        le=0.15,
        description="Expected annual property appreciation rate"
    )
    selling_costs_rate: float = Field(
        0.08,
        ge=0,
        le=0.15,
        description="Selling costs as % of sale price"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "down_payment": 100000,
                "loan_amount": 400000,
                "annual_interest_rate": 0.03,
                "loan_term_years": 20,
                "monthly_rent": 2000,
                "vacancy_rate": 0.05,
                "operating_expenses_annual": 6000,
                "holding_period_years": 10,
                "marginal_tax_rate": 0.30,
                "rental_regime": "location_nue"
            }
        }


class CashFlow(BaseModel):
    """Annual cash flow breakdown."""
    year: int = Field(..., description="Year number")
    rental_income: float = Field(..., description="Gross rental income")
    vacancy_loss: float = Field(..., description="Vacancy and credit loss")
    operating_expenses: float = Field(..., description="Operating expenses")
    debt_service: float = Field(..., description="Debt service (P+I)")
    pre_tax_cash_flow: float = Field(..., description="Pre-tax cash flow")
    taxes: float = Field(..., description="Income taxes and social charges")
    after_tax_cash_flow: float = Field(..., description="After-tax cash flow")
    cumulative_cash_flow: float = Field(..., description="Cumulative after-tax cash flow")
    property_value: Optional[float] = Field(None, description="Property value at year end")
    loan_balance: Optional[float] = Field(None, description="Remaining loan balance")

    class Config:
        json_schema_extra = {
            "example": {
                "year": 1,
                "rental_income": 24000,
                "vacancy_loss": 1200,
                "operating_expenses": 6000,
                "debt_service": 20000,
                "pre_tax_cash_flow": -3200,
                "taxes": 0,
                "after_tax_cash_flow": -3200,
                "cumulative_cash_flow": -3200
            }
        }


class Verdict(BaseModel):
    """60-second verdict output."""
    buy_pass: str = Field(..., description="BUY or PASS recommendation")
    dscr: float = Field(..., description="Debt Service Coverage Ratio")
    irr: float = Field(..., description="Internal Rate of Return (decimal)")
    tmc: float = Field(..., description="Total Monthly Cost (EUR)")
    price_verdict: str = Field(
        ...,
        description="Under-priced / Average / Overpriced"
    )
    legal_rent_status: str = Field(
        ...,
        description="Conformant – Low / Conformant – High / Non-conformant"
    )
    strategy_fits: List[dict] = Field(..., description="Strategy fit scores (top 3)")
    cash_flows: List[CashFlow] = Field(..., description="Year-by-year cash flows")
    environmental_risk_summary: str = Field(
        ...,
        description="Summary of environmental risks"
    )
    crime_risk_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Crime risk score (0-100)"
    )
    cap_rate: float = Field(..., description="Capitalization rate")
    coc_return: float = Field(..., description="Cash-on-cash return")
    npv: float = Field(..., description="Net present value")
    price_per_m2: float = Field(..., description="Price per m²")
    nowcast_value_per_m2: float = Field(..., description="Now-cast value per m²")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Verdict timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "buy_pass": "BUY",
                "dscr": 1.25,
                "irr": 0.085,
                "tmc": 1800,
                "price_verdict": "Under-priced",
                "legal_rent_status": "Conformant – High",
                "strategy_fits": [],
                "cash_flows": [],
                "environmental_risk_summary": "Low risk: No major concerns",
                "crime_risk_score": 35.0,
                "cap_rate": 0.045,
                "coc_return": 0.06,
                "npv": 50000,
                "price_per_m2": 10000,
                "nowcast_value_per_m2": 10500,
                "timestamp": "2025-09-30T12:00:00"
            }
        }


class StrategyFit(BaseModel):
    """Strategy fit score (0-100) with reasons."""
    strategy: str = Field(
        ...,
        description="Owner-occupier / Location nue / LMNP / Colocation / Value-Add"
    )
    score: float = Field(..., ge=0, le=100, description="Fit score (0-100)")
    reasons: List[str] = Field(..., description="Key reasons for score")
    pros: List[str] = Field(..., description="Advantages of this strategy")
    cons: List[str] = Field(..., description="Disadvantages of this strategy")

    class Config:
        json_schema_extra = {
            "example": {
                "strategy": "Location nue (unfurnished)",
                "score": 75.0,
                "reasons": ["Positive monthly cash flow", "Strong DSCR"],
                "pros": [
                    "30% flat tax abatement",
                    "Long-term tenant stability"
                ],
                "cons": [
                    "Lower rent vs furnished",
                    "Tenant protections favor long leases"
                ]
            }
        }