"""
Negotiation agent models.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class EmailDraft(BaseModel):
    """Gmail draft email."""
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body (plain text or HTML)")
    cc: Optional[str] = Field(None, description="CC recipients")
    draft_id: Optional[str] = Field(None, description="Gmail draft ID after creation")


class NegotiationPack(BaseModel):
    """Negotiation package with analytics."""
    property_address: str = Field(..., description="Property address")
    asking_price: float = Field(..., description="Asking price (EUR)")
    proposed_price: float = Field(..., description="Proposed offer price (EUR)")
    discount_percent: float = Field(..., description="Discount percentage")
    dscr: float = Field(..., description="Debt Service Coverage Ratio")
    irr: float = Field(..., description="Internal Rate of Return")
    price_verdict: str = Field(..., description="Price verdict (Under-priced/Average/Overpriced)")
    legal_rent_status: str = Field(..., description="Legal rent compliance status")
    dvf_median_per_m2: Optional[float] = Field(None, description="DVF median price/m²")
    comparable_sales: List[Dict] = Field(default_factory=list, description="Comparable sales")
    capital_alternative: Optional[str] = Field(None, description="Alternative investment comparison")
    justification: str = Field(..., description="Negotiation justification")

    class Config:
        json_schema_extra = {
            "example": {
                "property_address": "10 Rue de Rivoli, 75001 Paris",
                "asking_price": 500000,
                "proposed_price": 465000,
                "discount_percent": 7.0,
                "dscr": 1.15,
                "irr": 0.075,
                "price_verdict": "Average",
                "legal_rent_status": "Conformant – High",
                "dvf_median_per_m2": 10200,
                "justification": "Based on market comps and financial analysis"
            }
        }