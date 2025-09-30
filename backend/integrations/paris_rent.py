"""
Paris encadrement des loyers (rent control) API client.

API: https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/api/
"""

import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)


async def fetch_rent_cap(
    quartier: str,
    rooms: int,
    construction_period: str = "avant_1946",
    furnished: bool = False
) -> Dict[str, Any]:
    """
    Fetch Paris rent control ceiling data.

    Args:
        quartier: Paris neighborhood/quartier name
        rooms: Number of rooms
        construction_period: Construction period (avant_1946, 1946_1970, 1971_1990, apres_1990)
        furnished: Whether property is furnished

    Returns:
        dict: {
            "reference_rent_eur_m2": float,
            "ceiling_rent_eur_m2": float,
            "quartier": str,
            "epoque": str,
            "meuble": bool
        }

    Note:
        Data updated annually on July 1st. Cache for 1 year.
        Real API endpoint: https://opendata.paris.fr/explore/dataset/logement-encadrement-des-loyers/api/
    """
    logger.info(f"Fetching rent cap for {quartier}, {rooms} rooms, furnished={furnished}")

    # Map furnished flag to API meuble parameter
    meuble = "meublé" if furnished else "non meublé"

    # Map rooms to API piece_principale parameter
    if rooms == 1:
        piece = "1 pièce"
    elif rooms == 2:
        piece = "2 pièces"
    elif rooms == 3:
        piece = "3 pièces"
    elif rooms == 4:
        piece = "4 pièces"
    else:
        piece = "5 pièces et +"

    try:
        # Note: This is a placeholder. Real implementation would query:
        # https://opendata.paris.fr/api/records/1.0/search/?dataset=logement-encadrement-des-loyers

        async with httpx.AsyncClient() as client:
            # Placeholder - actual API call would look like:
            # params = {
            #     "dataset": "logement-encadrement-des-loyers",
            #     "q": f"nom_quartier:\"{quartier}\" AND piece_principale:\"{piece}\" AND meuble:\"{meuble}\"",
            #     "rows": 1
            # }
            # response = await client.get(
            #     "https://opendata.paris.fr/api/records/1.0/search/",
            #     params=params,
            #     timeout=30.0
            # )

            # For now, return placeholder data based on typical Paris rent caps
            # Real implementation would parse API response

            # Typical Paris rent caps (2025 estimates)
            base_reference = {
                "1 pièce": 30.0,
                "2 pièces": 26.0,
                "3 pièces": 24.0,
                "4 pièces": 22.0,
                "5 pièces et +": 20.0
            }

            reference_rent = base_reference.get(piece, 25.0)

            # Furnished premium (~20%)
            if furnished:
                reference_rent *= 1.2

            # Ceiling is reference + 20% (majoré)
            ceiling_rent = reference_rent * 1.2

            return {
                "reference_rent_eur_m2": round(reference_rent, 2),
                "ceiling_rent_eur_m2": round(ceiling_rent, 2),
                "quartier": quartier,
                "epoque": construction_period,
                "meuble": furnished,
                "note": "Placeholder data - real API integration needed"
            }

    except Exception as e:
        logger.error(f"Error fetching rent cap: {e}")
        # Return conservative estimates on error
        return {
            "reference_rent_eur_m2": 25.0,
            "ceiling_rent_eur_m2": 30.0,
            "quartier": quartier,
            "epoque": construction_period,
            "meuble": furnished,
            "error": str(e)
        }


def check_rent_compliance(
    property_rent_per_m2: float,
    ceiling_rent_per_m2: float,
    reference_rent_per_m2: float
) -> Dict[str, Any]:
    """
    Check if rent complies with Paris encadrement.

    Args:
        property_rent_per_m2: Actual property rent (EUR/m²)
        ceiling_rent_per_m2: Maximum allowed rent (EUR/m²)
        reference_rent_per_m2: Reference rent (EUR/m²)

    Returns:
        dict: {
            "compliant": bool,
            "status": str,  # "Conformant – Low / Conformant – High / Non-conformant"
            "percent_of_ceiling": float
        }
    """
    compliant = property_rent_per_m2 <= ceiling_rent_per_m2
    percent_of_ceiling = (property_rent_per_m2 / ceiling_rent_per_m2) * 100

    if not compliant:
        status = "Non-conformant"
    elif property_rent_per_m2 < reference_rent_per_m2:
        status = "Conformant – Low"
    else:
        status = "Conformant – High"

    return {
        "compliant": compliant,
        "status": status,
        "percent_of_ceiling": round(percent_of_ceiling, 1)
    }