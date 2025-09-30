"""
Risk assessment models (environmental and crime).
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class NaturalRisk(BaseModel):
    """Individual natural risk."""
    risk_type: str = Field(
        ...,
        description="Type of risk: flood, groundwater, seismicity, clay, radon, etc."
    )
    status: str = Field(..., description="Risk status: None / Low / Moderate / High")
    address_level: bool = Field(
        ...,
        description="Whether risk is at address level (vs commune level)"
    )
    description: Optional[str] = Field(None, description="Risk description")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_type": "flood",
                "status": "Moderate",
                "address_level": True,
                "description": "Property in flood zone with moderate risk"
            }
        }


class TechnologicalRisk(BaseModel):
    """Individual technological risk."""
    risk_type: str = Field(
        ...,
        description="Type of risk: ICPE, pipeline, soil pollution, etc."
    )
    status: str = Field(..., description="Risk status: None / Low / Moderate / High")
    address_level: bool = Field(..., description="Whether risk is at address level")
    distance_meters: Optional[float] = Field(
        None,
        description="Distance to risk source in meters"
    )
    description: Optional[str] = Field(None, description="Risk description")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_type": "ICPE",
                "status": "Low",
                "address_level": False,
                "distance_meters": 500,
                "description": "Industrial site 500m away"
            }
        }


class EnvironmentalRisk(BaseModel):
    """Complete environmental risk assessment."""
    postal_code: str = Field(..., pattern=r"^\d{5}$", description="Postal code")
    address: Optional[str] = Field(None, description="Full address")
    natural_risks: List[NaturalRisk] = Field(
        default_factory=list,
        description="List of natural risks"
    )
    technological_risks: List[TechnologicalRisk] = Field(
        default_factory=list,
        description="List of technological risks"
    )
    overall_risk_level: str = Field(
        ...,
        description="Overall risk level: Low / Moderate / High / Severe"
    )
    summary: str = Field(..., description="Summary of environmental risks")
    source_url: Optional[str] = Field(
        None,
        description="Link to Géorisques report"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "postal_code": "75001",
                "address": "10 Rue de Rivoli, 75001 Paris",
                "natural_risks": [
                    {
                        "risk_type": "flood",
                        "status": "Low",
                        "address_level": True,
                        "description": "Low flood risk"
                    }
                ],
                "technological_risks": [],
                "overall_risk_level": "Low",
                "summary": "Low overall risk: Minimal natural and no technological risks",
                "source_url": "https://www.georisques.gouv.fr/..."
            }
        }


class CrimeRisk(BaseModel):
    """Crime risk assessment."""
    postal_code: str = Field(..., pattern=r"^\d{5}$", description="Postal code")
    crime_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Normalized crime risk score (0-100, lower is better)"
    )
    categories: Dict[str, float] = Field(
        ...,
        description="Crime rates by category (per 1,000 inhabitants)"
    )
    national_comparison: str = Field(
        ...,
        description="Comparison to national median: Below / Average / Above"
    )
    summary: str = Field(..., description="Summary of crime risk")

    class Config:
        json_schema_extra = {
            "example": {
                "postal_code": "75001",
                "crime_score": 35.0,
                "categories": {
                    "burglary": 5.2,
                    "theft": 12.5,
                    "vehicle_theft": 3.8,
                    "assault": 2.1
                },
                "national_comparison": "Above",
                "summary": "Above-average crime rates, primarily property crimes in tourist area"
            }
        }


class RiskSummary(BaseModel):
    """Combined risk summary."""
    environmental_risk: EnvironmentalRisk
    crime_risk: CrimeRisk
    overall_risk_assessment: str = Field(
        ...,
        description="Overall risk assessment combining all factors"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "environmental_risk": {
                    "postal_code": "75001",
                    "overall_risk_level": "Low",
                    "summary": "Low overall risk",
                    "natural_risks": [],
                    "technological_risks": []
                },
                "crime_risk": {
                    "postal_code": "75001",
                    "crime_score": 35.0,
                    "categories": {},
                    "national_comparison": "Above",
                    "summary": "Above-average crime"
                },
                "overall_risk_assessment": "Moderate: Low environmental risk but elevated crime in tourist area"
            }
        }