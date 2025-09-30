"""
Legal and compliance models.
"""

from pydantic import BaseModel, Field
from typing import Optional


class LegalRentCheck(BaseModel):
    """Paris encadrement des loyers (rent control) check."""
    reference_rent_eur_m2: float = Field(
        ...,
        description="Reference rent (EUR/m²)"
    )
    ceiling_rent_eur_m2: float = Field(
        ...,
        description="Maximum allowed rent (majored ceiling, EUR/m²)"
    )
    property_rent_eur_m2: float = Field(
        ...,
        description="Actual property rent (EUR/m²)"
    )
    compliant: bool = Field(
        ...,
        description="Whether rent complies with encadrement"
    )
    status: str = Field(
        ...,
        description="Conformant – Low / Conformant – High / Non-conformant"
    )
    complement_de_loyer: Optional[float] = Field(
        None,
        description="Rent supplement if justified (EUR/month)"
    )
    quartier: str = Field(..., description="Paris neighborhood/quartier")
    construction_period: Optional[str] = Field(
        None,
        description="Construction period category"
    )
    furnished: bool = Field(..., description="Whether property is furnished")

    class Config:
        json_schema_extra = {
            "example": {
                "reference_rent_eur_m2": 28.50,
                "ceiling_rent_eur_m2": 34.20,
                "property_rent_eur_m2": 32.00,
                "compliant": True,
                "status": "Conformant – High",
                "quartier": "Louvre",
                "furnished": False
            }
        }


class ZoneTendue(BaseModel):
    """Zone tendue (tight market) status."""
    postal_code: str = Field(..., pattern=r"^\d{5}$", description="Postal code")
    is_zone_tendue: bool = Field(..., description="Whether area is zone tendue")
    rent_control_applies: bool = Field(
        ...,
        description="Whether rent control applies"
    )
    restrictions: list = Field(
        default_factory=list,
        description="List of applicable restrictions"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "postal_code": "75001",
                "is_zone_tendue": True,
                "rent_control_applies": True,
                "restrictions": [
                    "Encadrement des loyers applies",
                    "Notice period restrictions"
                ]
            }
        }


class Compliance(BaseModel):
    """Overall compliance status."""
    legal_rent: LegalRentCheck
    zone_tendue: ZoneTendue
    dpe_compliant: bool = Field(
        ...,
        description="Whether DPE meets minimum standards"
    )
    dpe_grade: Optional[str] = Field(
        None,
        pattern=r"^[A-G]$",
        description="DPE energy grade"
    )
    dpe_issues: list = Field(
        default_factory=list,
        description="List of DPE-related issues"
    )
    overall_compliant: bool = Field(
        ...,
        description="Whether property is overall compliant"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "legal_rent": {
                    "reference_rent_eur_m2": 28.50,
                    "ceiling_rent_eur_m2": 34.20,
                    "property_rent_eur_m2": 32.00,
                    "compliant": True,
                    "status": "Conformant – High",
                    "quartier": "Louvre",
                    "furnished": False
                },
                "zone_tendue": {
                    "postal_code": "75001",
                    "is_zone_tendue": True,
                    "rent_control_applies": True,
                    "restrictions": []
                },
                "dpe_compliant": True,
                "dpe_grade": "D",
                "dpe_issues": [],
                "overall_compliant": True
            }
        }