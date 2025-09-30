"""
Research agent for property data gathering.

MIRROR: use-cases/pydantic-ai/examples/main_agent_reference/research_agent.py
"""

import logging
from typing import Dict, Any, List

from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

from backend.agents.providers import get_llm_model
from backend.agents.research.prompts import RESEARCH_SYSTEM_PROMPT
from backend.agents.research import tools
from backend.integrations import dvf, paris_rent

logger = logging.getLogger(__name__)


@dataclass
class ResearchAgentDependencies:
    """Dependencies for the research agent."""
    brave_api_key: str
    session_id: str = None


# Create research agent (NO result_type - default to string)
research_agent = Agent(
    get_llm_model(),
    deps_type=ResearchAgentDependencies,
    system_prompt=RESEARCH_SYSTEM_PROMPT
)


@research_agent.tool
async def search_listings(
    ctx: RunContext[ResearchAgentDependencies],
    query: str,
    max_results: int = 10
) -> List[Dict[str, Any]]:
    """
    Search for property listings using Brave Search.

    Args:
        query: Search query (e.g., "appartement paris 2 pièces 75001")
        max_results: Maximum number of results (1-20)

    Returns:
        List of search results with title, URL, description
    """
    return await tools.search_listings_tool(
        api_key=ctx.deps.brave_api_key,
        query=query,
        max_results=max_results
    )


@research_agent.tool
async def fetch_dvf_comparables(
    ctx: RunContext[ResearchAgentDependencies],
    address: str,
    postal_code: str,
    radius_km: float = 0.5
) -> Dict[str, Any]:
    """
    Fetch DVF comparable sales and calculate median price.

    Args:
        address: Property address
        postal_code: 5-digit postal code
        radius_km: Search radius in kilometers

    Returns:
        Dictionary with comps and median_price_per_m2
    """
    comps = await tools.fetch_dvf_comps_tool(
        address=address,
        postal_code=postal_code,
        radius_km=radius_km
    )

    median_price = dvf.calculate_median_price_per_m2(comps)

    return {
        "comps": comps,
        "median_price_per_m2": median_price,
        "count": len(comps)
    }


@research_agent.tool
async def check_paris_rent_control(
    ctx: RunContext[ResearchAgentDependencies],
    quartier: str,
    rooms: int,
    furnished: bool = False,
    property_rent_per_m2: float = None
) -> Dict[str, Any]:
    """
    Check Paris rent control (encadrement des loyers) compliance.

    Args:
        quartier: Paris neighborhood name
        rooms: Number of rooms
        furnished: Whether property is furnished
        property_rent_per_m2: Optional actual rent to check compliance

    Returns:
        Dictionary with reference_rent, ceiling_rent, and compliance status
    """
    rent_cap = await tools.check_rent_cap_tool(
        quartier=quartier,
        rooms=rooms,
        furnished=furnished
    )

    result = {
        "reference_rent_eur_m2": rent_cap["reference_rent_eur_m2"],
        "ceiling_rent_eur_m2": rent_cap["ceiling_rent_eur_m2"],
        "quartier": quartier,
        "rooms": rooms,
        "furnished": furnished
    }

    # Check compliance if property rent provided
    if property_rent_per_m2 is not None:
        compliance = paris_rent.check_rent_compliance(
            property_rent_per_m2=property_rent_per_m2,
            ceiling_rent_per_m2=rent_cap["ceiling_rent_eur_m2"],
            reference_rent_per_m2=rent_cap["reference_rent_eur_m2"]
        )
        result.update(compliance)

    return result


@research_agent.tool
async def assess_property_risks(
    ctx: RunContext[ResearchAgentDependencies],
    postal_code: str,
    address: str = None
) -> Dict[str, Any]:
    """
    Assess environmental and crime risks for a property.

    Args:
        postal_code: 5-digit postal code
        address: Optional full address for more precise risk data

    Returns:
        Dictionary with environmental and crime risk summaries
    """
    # Fetch environmental risks
    env_risks = await tools.fetch_environmental_risks_tool(
        postal_code=postal_code,
        address=address
    )

    # Fetch crime statistics
    crime_stats = await tools.fetch_crime_stats_tool(postal_code=postal_code)

    return {
        "environmental": {
            "risk_level": env_risks.get("overall_risk_level", "Unknown"),
            "summary": env_risks.get("summary", ""),
            "natural_risks_count": len(env_risks.get("natural_risks", [])),
            "technological_risks_count": len(env_risks.get("technological_risks", [])),
            "source_url": env_risks.get("source_url", "")
        },
        "crime": {
            "score": crime_stats.get("crime_score", 50.0),
            "summary": crime_stats.get("summary", ""),
            "national_comparison": crime_stats.get("national_comparison", "Average"),
            "categories": crime_stats.get("categories", {})
        }
    }


# Convenience function
def create_research_agent_with_deps(brave_api_key: str, session_id: str = None):
    """
    Create research agent with dependencies.

    Args:
        brave_api_key: Brave Search API key
        session_id: Optional session ID

    Returns:
        Configured research agent
    """
    return research_agent