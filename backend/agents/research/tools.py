"""
Pure tool functions for research agent.
"""

import logging
from typing import List, Dict, Any, Optional

from backend.integrations import brave, dvf, paris_rent, georisques, crime_data

logger = logging.getLogger(__name__)


async def search_listings_tool(
    api_key: str,
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for property listings using Brave Search.

    Args:
        api_key: Brave Search API key
        query: Search query (e.g., "appartement paris 75001")
        max_results: Maximum results to return

    Returns:
        List of search results
    """
    try:
        results = await brave.search_web(
            api_key=api_key,
            query=query,
            count=min(max_results, 20)
        )
        logger.info(f"Found {len(results)} listings for: {query}")
        return results
    except Exception as e:
        logger.error(f"Error searching listings: {e}")
        return []


async def fetch_dvf_comps_tool(
    address: str,
    postal_code: str,
    radius_km: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Fetch DVF comparable sales.

    Args:
        address: Property address
        postal_code: Postal code
        radius_km: Search radius in km

    Returns:
        List of comparable sales
    """
    try:
        comps = await dvf.fetch_dvf_comps(
            address=address,
            postal_code=postal_code,
            radius_km=radius_km
        )
        logger.info(f"Found {len(comps)} DVF comps for {postal_code}")
        return comps
    except Exception as e:
        logger.error(f"Error fetching DVF comps: {e}")
        return []


async def check_rent_cap_tool(
    quartier: str,
    rooms: int,
    furnished: bool = False
) -> Dict[str, Any]:
    """
    Check Paris rent control cap.

    Args:
        quartier: Paris neighborhood
        rooms: Number of rooms
        furnished: Whether property is furnished

    Returns:
        Rent cap data
    """
    try:
        rent_cap = await paris_rent.fetch_rent_cap(
            quartier=quartier,
            rooms=rooms,
            furnished=furnished
        )
        logger.info(f"Rent cap for {quartier}: {rent_cap.get('ceiling_rent_eur_m2')} EUR/m²")
        return rent_cap
    except Exception as e:
        logger.error(f"Error fetching rent cap: {e}")
        return {
            "reference_rent_eur_m2": 25.0,
            "ceiling_rent_eur_m2": 30.0,
            "error": str(e)
        }


async def fetch_environmental_risks_tool(
    postal_code: str,
    address: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch environmental and technological risks.

    Args:
        postal_code: Postal code
        address: Optional full address

    Returns:
        Risk data
    """
    try:
        risks = await georisques.fetch_environmental_risks(
            postal_code=postal_code,
            address=address
        )
        logger.info(f"Environmental risk level for {postal_code}: {risks.get('overall_risk_level')}")
        return risks
    except Exception as e:
        logger.error(f"Error fetching environmental risks: {e}")
        return {
            "overall_risk_level": "Unknown",
            "summary": f"Error: {str(e)}",
            "natural_risks": [],
            "technological_risks": []
        }


async def fetch_crime_stats_tool(postal_code: str) -> Dict[str, Any]:
    """
    Fetch crime statistics.

    Args:
        postal_code: Postal code

    Returns:
        Crime data
    """
    try:
        crime_stats = await crime_data.fetch_crime_stats(postal_code=postal_code)
        logger.info(f"Crime score for {postal_code}: {crime_stats.get('crime_score')}")
        return crime_stats
    except Exception as e:
        logger.error(f"Error fetching crime stats: {e}")
        return {
            "crime_score": 50.0,
            "summary": f"Error: {str(e)}",
            "categories": {}
        }