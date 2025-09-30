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
    radius_km: float = 0.5,
    min_date: Optional[str] = None,
    property_type: str = "appartement"
) -> List[Dict[str, Any]]:
    """
    Fetch DVF comparable sales data.

    Args:
        address: Property address
        postal_code: 5-digit postal code
        radius_km: Search radius in kilometers
        min_date: Minimum sale date (YYYY-MM-DD), defaults to 2 years ago
        property_type: Type of property (appartement, maison)

    Returns:
        List of comparable sales

    Note:
        DVF data is updated every 6 months (April, October).
        This is a simplified implementation. Real implementation would use
        the official DVF API or data.gouv.fr API.
    """
    if min_date is None:
        # Default to 2 years ago
        min_date = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")

    logger.info(f"Fetching DVF comps for {postal_code} within {radius_km}km")

    # Note: This is a placeholder. Real implementation would query:
    # https://api.gouv.fr/les-api/api-donnees-foncieres
    # or DVF+ API: https://www.data.gouv.fr/dataservices/api-dvf-trouvez-les-valeurs-de-ventes-et-encore/

    try:
        # Placeholder: In real implementation, would make API call
        # For now, return example structure
        comps = []

        # Example structure of what would be returned:
        # comps.append({
        #     "id_mutation": "2024-12345",
        #     "date_mutation": "2024-06-15",
        #     "adresse": "12 Rue Example",
        #     "code_postal": postal_code,
        #     "type_local": "Appartement",
        #     "surface_reelle_bati": 48.5,
        #     "nombre_pieces_principales": 2,
        #     "valeur_fonciere": 485000,
        #     "price_per_m2": 10000
        # })

        logger.info(f"Found {len(comps)} comps (placeholder - API not yet implemented)")

        return comps

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