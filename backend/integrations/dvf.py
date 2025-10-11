"""
DVF (Demandes de Valeurs Foncières) API client for French property transaction data.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import httpx

logger = logging.getLogger(__name__)


async def fetch_dvf_comps(
    address: str,
    postal_code: str,
    surface: float,
    radius_km: float = 0.5,
    min_date: Optional[str] = None,
    property_type: str = "Appartement"
) -> List[Dict[str, Any]]:
    """
    Fetch DVF comparable sales data from api.cquest.org.

    Args:
        address: Property address
        postal_code: 5-digit postal code
        surface: Property surface in m²
        radius_km: Search radius in kilometers
        min_date: Minimum sale date (YYYY-MM-DD), defaults to 2 years ago
        property_type: Type of property (Appartement, Maison)

    Returns:
        List of comparable sales

    Note:
        DVF data is updated every 6 months (April, October).
        Uses api.cquest.org DVF API
    """
    if min_date is None:
        # Default to 2 years ago
        min_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

    logger.info(f"Fetching DVF comps for {postal_code} within {radius_km}km, surface {surface}m²")

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            # Use api.cquest.org DVF API
            url = "https://api.cquest.org/dvf"

            min_surface = surface * 0.7
            max_surface = surface * 1.3

            params = {
                "code_postal": postal_code,
                "type_local": property_type
            }

            response = await client.get(url, params=params)

            if response.status_code != 200:
                logger.warning(f"DVF API returned status {response.status_code}")
                return []

            data = response.json()

            # API returns {"resultats": [...]} or {"features": [...]}
            results = data.get("resultats", data.get("features", []))

            if not results:
                logger.warning(f"No DVF results for {postal_code}")
                return []

            comps = []
            for record in results:
                # Extract fields (note: surface_relle_bati has typo in API)
                surface_bati = record.get("surface_relle_bati") or record.get("surface_reelle_bati")
                valeur = record.get("valeur_fonciere")
                date_mutation = record.get("date_mutation")

                # Filter by date and surface
                if date_mutation and date_mutation < min_date:
                    continue

                if not surface_bati or not valeur:
                    continue

                # Filter by surface range (±30%)
                if surface_bati < min_surface or surface_bati > max_surface:
                    continue

                # Only include valid transactions
                if valeur > 0 and surface_bati > 0:
                    price_per_m2 = valeur / surface_bati

                    comps.append({
                        "id_mutation": record.get("reference_document", ""),
                        "date_mutation": date_mutation,
                        "adresse": f"{record.get('numero_voie', '')} {record.get('type_voie', '')} {record.get('voie', '')}".strip(),
                        "code_postal": record.get("code_postal"),
                        "commune": record.get("commune"),
                        "type_local": record.get("type_local"),
                        "surface_reelle_bati": surface_bati,
                        "nombre_pieces_principales": record.get("nombre_pieces_principales"),
                        "valeur_fonciere": valeur,
                        "price_per_m2": price_per_m2
                    })

            logger.info(f"Found {len(comps)} DVF comps for {postal_code} (from {len(results)} total results)")
            return comps

    except httpx.TimeoutException:
        logger.warning(f"DVF API timeout for {postal_code}")
        return []
    except Exception as e:
        logger.error(f"Error fetching DVF comps: {e}")
        return []


def calculate_median_price_per_m2(comps: List[Dict[str, Any]]) -> float:
    """
    Calculate median price per m² from comparable sales.

    Args:
        comps: List of comparable sales

    Returns:
        float: Median price per m²
    """
    if not comps:
        return 0.0

    prices_per_m2 = []
    for comp in comps:
        if "price_per_m2" in comp:
            prices_per_m2.append(comp["price_per_m2"])
        elif "valeur_fonciere" in comp and "surface_reelle_bati" in comp:
            surface = comp["surface_reelle_bati"]
            if surface > 0:
                prices_per_m2.append(comp["valeur_fonciere"] / surface)

    if not prices_per_m2:
        return 0.0

    # Calculate median
    sorted_prices = sorted(prices_per_m2)
    n = len(sorted_prices)
    if n % 2 == 0:
        median = (sorted_prices[n // 2 - 1] + sorted_prices[n // 2]) / 2
    else:
        median = sorted_prices[n // 2]

    return median