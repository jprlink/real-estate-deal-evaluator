"""
Property and address models.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class Address(BaseModel):
    """Property address."""
    street: str = Field(..., description="Street address")
    city: str = Field(default="Paris", description="City name")
    postal_code: str = Field(..., pattern=r"^\d{5}$", description="5-digit postal code")
    quartier: Optional[str] = Field(None, description="Paris neighborhood/quartier")

    class Config:
        json_schema_extra = {
            "example": {
                "street": "10 Rue de Rivoli",
                "city": "Paris",
                "postal_code": "75001",
                "quartier": "Louvre"
            }
        }


class Property(BaseModel):
    """Property details."""
    address: Address
    price: float = Field(..., gt=0, description="Property price in EUR")
    surface: float = Field(..., gt=0, description="Living surface in m²")
    rooms: int = Field(..., ge=1, description="Number of rooms")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms")
    construction_year: Optional[int] = Field(
        None,
        ge=1800,
        le=2030,
        description="Year of construction"
    )
    dpe: Optional[str] = Field(
        None,
        pattern=r"^[A-G]$",
        description="DPE energy grade (A-G)"
    )
    furnished: bool = Field(default=False, description="Whether property is furnished")
    floor: Optional[int] = Field(None, description="Floor number")
    total_floors: Optional[int] = Field(None, description="Total floors in building")
    has_elevator: Optional[bool] = Field(None, description="Building has elevator")
    parking: Optional[bool] = Field(None, description="Parking included")
    balcony: Optional[bool] = Field(None, description="Has balcony/terrace")

    class Config:
        json_schema_extra = {
            "example": {
                "address": {
                    "street": "10 Rue de Rivoli",
                    "city": "Paris",
                    "postal_code": "75001"
                },
                "price": 500000,
                "surface": 50,
                "rooms": 2,
                "bedrooms": 1,
                "construction_year": 1900,
                "dpe": "D",
                "furnished": False
            }
        }


class Listing(BaseModel):
    """Property listing information."""
    property: Property
    listing_url: Optional[str] = Field(None, description="Original listing URL")
    listing_date: Optional[date] = Field(None, description="Date listing was posted")
    days_on_market: Optional[int] = Field(None, ge=0, description="Days on market")
    price_history: Optional[list] = Field(
        default_factory=list,
        description="Price change history"
    )
    description: Optional[str] = Field(None, description="Listing description")
    photos: Optional[list] = Field(default_factory=list, description="Photo URLs")

    class Config:
        json_schema_extra = {
            "example": {
                "property": {
                    "address": {
                        "street": "10 Rue de Rivoli",
                        "city": "Paris",
                        "postal_code": "75001"
                    },
                    "price": 500000,
                    "surface": 50,
                    "rooms": 2,
                    "bedrooms": 1
                },
                "listing_date": "2025-01-01",
                "days_on_market": 30
            }
        }