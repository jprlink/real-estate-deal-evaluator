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
    projection_years: int = Field(default=30, ge=1, le=50)  # Number of years to project cash flow
    renovation_costs: float = Field(default=0, ge=0)  # Optional renovation costs before renting


class CashFlowYear(BaseModel):
    """Cash flow data for a single year."""
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
    appreciation_rate: Optional[float] = None  # Annual appreciation rate
    appreciation_rate_display: Optional[str] = None  # Display format (e.g., "+2.3%")


class StrategyFit(BaseModel):
    """Strategy fit scoring."""
    strategy: str
    score: float
    pros: List[str]
    cons: List[str]


class RentBand(BaseModel):
    """Rent control band information for legal compliance or market estimate."""
    min_rent: float  # Minimum rent per m² (legal control or market estimate)
    max_rent: float  # Maximum rent per m² (legal control or market estimate)
    median_rent: float  # Median/reference rent per m²
    property_rent_per_m2: float  # Actual rent per m² for this property
    total_monthly_rent: float  # Total monthly rent in euros
    surface: float  # Property surface in m²
    is_compliant: bool  # Whether property rent is within limits
    compliance_percentage: float  # Where property rent sits in the band (0-100%)
    is_estimate: bool = False  # True if using regional estimate, False if legal control


class PurchaseCosts(BaseModel):
    """Detailed breakdown of French property purchase costs (frais d'acquisition)."""
    down_payment: float  # Initial equity payment
    renovation_costs: float  # Costs for repairs/improvements
    registration_duties: float  # Droits d'enregistrement (transfer taxes) ~5.8%
    notaire_fees: float  # Actual notaire professional fees ~1%
    disbursements: float  # Administrative costs ~0.4%
    mortgage_fees: float  # Additional fees if mortgage ~0.4%
    total_fees: float  # Total of all fees (excluding down payment and renovation)
    total_cash_required: float  # Total cash needed at closing


class PropertyEvaluationResponse(BaseModel):
    """Response schema for property evaluation."""
    verdict: str  # "BUY", "CAUTION", "PASS"
    price_verdict: str  # "Under-priced", "Average", "Overpriced"
    legal_rent_status: str  # "Conformant – Low", "Conformant – High", "Non-conformant"
    metrics: FinancialMetrics
    strategy_fits: List[StrategyFit]
    summary: str
    cash_flow_projections: List[CashFlowYear] = []  # Customizable-year cash flow projections
    appreciation_source: Optional[str] = None  # Data source for appreciation rate
    rent_band: Optional[RentBand] = None  # Legal rent band information
    city: Optional[str] = None  # Detected city from postal code
    price_source: Optional[str] = None  # Data source for price verdict (DVF or fallback)
    purchase_costs: Optional[PurchaseCosts] = None  # Detailed breakdown of purchase costs


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