"""
Research agent models.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ListingData(BaseModel):
    """Parsed listing data."""
    address: str = Field(..., description="Property address")
    postal_code: str = Field(..., pattern=r"^\d{5}$", description="Postal code")
    price: float = Field(..., gt=0, description="Property price (EUR)")
    surface: float = Field(..., gt=0, description="Surface area (m²)")
    rooms: int = Field(..., ge=1, description="Number of rooms")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms")
    dpe: Optional[str] = Field(None, pattern=r"^[A-G]$", description="DPE grade")
    furnished: bool = Field(default=False, description="Is furnished")
    days_on_market: Optional[int] = Field(None, ge=0, description="Days on market")
    listing_url: Optional[str] = Field(None, description="Original listing URL")


class DVFComp(BaseModel):
    """DVF comparable sale."""
    address: str = Field(..., description="Property address")
    sale_date: str = Field(..., description="Sale date (YYYY-MM-DD)")
    price: float = Field(..., description="Sale price (EUR)")
    surface: float = Field(..., description="Surface area (m²)")
    price_per_m2: float = Field(..., description="Price per m²")
    rooms: Optional[int] = Field(None, description="Number of rooms")
    property_type: str = Field(..., description="Property type (appartement, maison)")


class RiskSummary(BaseModel):
    """Risk assessment summary."""
    environmental_risk_level: str = Field(
        ...,
        description="Overall environmental risk: Low / Moderate / High / Severe"
    )
    environmental_summary: str = Field(..., description="Environmental risks summary")
    crime_score: float = Field(..., ge=0, le=100, description="Crime risk score (0-100)")
    crime_summary: str = Field(..., description="Crime risk summary")
    natural_risks_count: int = Field(..., description="Number of natural risks")
    technological_risks_count: int = Field(..., description="Number of technological risks")


class ResearchResult(BaseModel):
    """Complete research results."""
    listing: Optional[ListingData] = Field(None, description="Parsed listing data")
    dvf_comps: List[DVFComp] = Field(default_factory=list, description="DVF comparables")
    dvf_median_price_per_m2: Optional[float] = Field(
        None,
        description="Median price/m² from comps"
    )
    legal_rent_reference: Optional[float] = Field(
        None,
        description="Reference rent (EUR/m²)"
    )
    legal_rent_ceiling: Optional[float] = Field(
        None,
        description="Ceiling rent (EUR/m²)"
    )
    legal_rent_compliant: Optional[bool] = Field(
        None,
        description="Whether rent is compliant"
    )
    risk_summary: Optional[RiskSummary] = Field(None, description="Risk assessment")
    zone_tendue: bool = Field(default=True, description="Is zone tendue (Paris)")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Research timestamp"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "listing": {
                    "address": "10 Rue de Rivoli",
                    "postal_code": "75001",
                    "price": 500000,
                    "surface": 50,
                    "rooms": 2,
                    "bedrooms": 1
                },
                "dvf_median_price_per_m2": 10500,
                "legal_rent_reference": 28.5,
                "legal_rent_ceiling": 34.2,
                "legal_rent_compliant": True
            }
        }