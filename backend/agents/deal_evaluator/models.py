"""
Deal evaluator agent models.

Note: Verdict and StrategyFit models are in backend/models/financial.py
This file contains additional models specific to the evaluator agent.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EvaluationRequest(BaseModel):
    """Request for property evaluation."""
    # Property details
    address: str = Field(..., description="Property address")
    postal_code: str = Field(..., pattern=r"^\d{5}$", description="Postal code")
    price: float = Field(..., gt=0, description="Property price (EUR)")
    surface: float = Field(..., gt=0, description="Surface area (m²)")
    rooms: int = Field(..., ge=1, description="Number of rooms")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms")
    construction_year: Optional[int] = Field(None, description="Year of construction")
    dpe: Optional[str] = Field(None, pattern=r"^[A-G]$", description="DPE grade")
    furnished: bool = Field(default=False, description="Is furnished")
    quartier: Optional[str] = Field(None, description="Paris neighborhood")

    # Financial inputs
    down_payment: float = Field(..., ge=0, description="Down payment (EUR)")
    loan_amount: float = Field(..., ge=0, description="Loan amount (EUR)")
    annual_interest_rate: float = Field(..., ge=0, le=0.15, description="Annual interest rate")
    loan_term_years: int = Field(..., ge=1, le=30, description="Loan term (years)")
    monthly_rent: float = Field(..., ge=0, description="Expected monthly rent (EUR)")
    vacancy_rate: float = Field(0.05, ge=0, le=0.30, description="Vacancy rate")
    operating_expenses_annual: float = Field(..., ge=0, description="Annual operating expenses (EUR)")
    holding_period_years: int = Field(10, ge=1, le=30, description="Holding period (years)")
    marginal_tax_rate: float = Field(0.30, ge=0, le=0.50, description="Marginal tax rate")
    rental_regime: str = Field(default="location_nue", description="Rental regime")

    # Optional
    listing_url: Optional[str] = Field(None, description="Original listing URL")
    request_negotiation_draft: bool = Field(default=False, description="Create negotiation email draft")
    recipient_email: Optional[str] = Field(None, description="Email for negotiation draft")

    class Config:
        json_schema_extra = {
            "example": {
                "address": "10 Rue de Rivoli",
                "postal_code": "75001",
                "price": 500000,
                "surface": 50,
                "rooms": 2,
                "bedrooms": 1,
                "dpe": "D",
                "furnished": False,
                "quartier": "Louvre",
                "down_payment": 100000,
                "loan_amount": 400000,
                "annual_interest_rate": 0.03,
                "loan_term_years": 20,
                "monthly_rent": 2000,
                "vacancy_rate": 0.05,
                "operating_expenses_annual": 6000,
                "holding_period_years": 10
            }
        }


class EvaluationResult(BaseModel):
    """Complete evaluation result with verdict."""
    verdict: dict = Field(..., description="60-second verdict")
    research_data: Optional[dict] = Field(None, description="Research agent data")
    negotiation_draft_id: Optional[str] = Field(None, description="Gmail draft ID if requested")
    timestamp: datetime = Field(default_factory=datetime.now, description="Evaluation timestamp")
    execution_time_seconds: Optional[float] = Field(None, description="Execution time")