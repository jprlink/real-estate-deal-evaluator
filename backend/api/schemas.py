"""
Request and response schemas for API endpoints.
"""

from typing import Optional, List
from pydantic import BaseModel, Field


class PropertyEvaluationRequest(BaseModel):
    """Request schema for property evaluation."""
    address: str  # Can be quartier, city, or full address
    postal_code: str = Field(..., pattern=r"^\d{5}$")  # Any French postal code (5 digits)
    price: float = Field(..., gt=0)
    surface: float = Field(..., gt=0)
    rooms: int = Field(..., ge=1)
    bedrooms: int = Field(..., ge=1)
    floor: Optional[int] = None
    dpe: Optional[str] = Field(None, pattern=r"^[A-G]$")
    down_payment: float = Field(..., ge=0)
    loan_amount: float = Field(..., ge=0)
    annual_rate: float = Field(..., ge=0, le=1)
    loan_term: int = Field(..., ge=1, le=50)
    monthly_rent: float = Field(..., gt=0)


class FinancialMetrics(BaseModel):
    """Financial metrics from evaluation."""
    monthly_payment: float
    noi: float
    dscr: float
    cap_rate: float
    cash_on_cash: float
    irr: float
    price_per_m2: float
    ltv: float


class StrategyFit(BaseModel):
    """Strategy fit scoring."""
    strategy: str
    score: float
    pros: List[str]
    cons: List[str]


class PropertyEvaluationResponse(BaseModel):
    """Response schema for property evaluation."""
    verdict: str  # "BUY", "CAUTION", "PASS"
    price_verdict: str  # "Under-priced", "Average", "Overpriced"
    legal_rent_status: str  # "Conformant – Low", "Conformant – High", "Non-conformant"
    metrics: FinancialMetrics
    strategy_fits: List[StrategyFit]
    summary: str


class ResearchRequest(BaseModel):
    """Request schema for property research."""
    address: str
    postal_code: str


class ResearchResponse(BaseModel):
    """Response schema for property research."""
    dvf_comps: List[dict]
    rent_cap: dict
    environmental_risks: dict
    crime_data: dict
    summary: str


class NegotiationRequest(BaseModel):
    """Request schema for negotiation email."""
    property_address: str
    asking_price: float
    offered_price: float
    dscr: float
    irr: float
    recipient_email: Optional[str] = None


class NegotiationResponse(BaseModel):
    """Response schema for negotiation email."""
    draft_created: bool
    draft_id: Optional[str] = None
    email_preview: str