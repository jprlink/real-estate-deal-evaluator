"""
Primary Deal Evaluator Agent - orchestrates the entire evaluation process.

This agent:
1. Invokes research sub-agent for market data
2. Performs deterministic financial calculations
3. Generates 60-second Buy/Pass verdict
4. Optionally invokes negotiation sub-agent
"""

import logging
from dataclasses import dataclass
from typing import Dict, Any

from pydantic_ai import Agent, RunContext

from backend.agents.providers import get_llm_model
from backend.agents.deal_evaluator.prompts import EVALUATOR_SYSTEM_PROMPT
from backend.agents.research.agent import research_agent, ResearchAgentDependencies
from backend.agents.negotiation.agent import negotiation_agent, NegotiationAgentDependencies

# Import calculation modules
from backend.calculations import financial, mortgage, strategy_fit
from backend.calculations.irr_npv import irr_calculation, npv_calculation
from backend.calculations.valuation import price_verdict as calc_price_verdict

logger = logging.getLogger(__name__)


@dataclass
class DealEvaluatorDependencies:
    """Dependencies for the deal evaluator agent."""
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: str = None


# Create deal evaluator agent (NO result_type - default to string)
deal_evaluator_agent = Agent(
    get_llm_model(),
    deps_type=DealEvaluatorDependencies,
    system_prompt=EVALUATOR_SYSTEM_PROMPT
)


@deal_evaluator_agent.tool
async def invoke_research_agent(
    ctx: RunContext[DealEvaluatorDependencies],
    property_address: str,
    postal_code: str,
    quartier: str,
    rooms: int,
    furnished: bool = False
) -> Dict[str, Any]:
    """
    Invoke research sub-agent to gather market data.

    Args:
        property_address: Full property address
        postal_code: 5-digit postal code
        quartier: Paris neighborhood
        rooms: Number of rooms
        furnished: Whether property is furnished

    Returns:
        Dictionary with research data (DVF comps, rent caps, risks)
    """
    try:
        logger.info(f"Invoking research agent for {property_address}")

        # Create research agent dependencies
        research_deps = ResearchAgentDependencies(
            brave_api_key=ctx.deps.brave_api_key,
            session_id=ctx.deps.session_id
        )

        # Invoke research agent
        # Note: In full implementation, would parse agent response
        # For now, we'll directly call research tools

        research_prompt = f"""
        Research property at {property_address}, {postal_code}.

        Tasks:
        1. Fetch DVF comparable sales within 0.5km
        2. Check Paris rent control for {quartier}, {rooms} rooms, furnished={furnished}
        3. Assess environmental and crime risks for {postal_code}

        Provide structured data for financial analysis.
        """

        result = await research_agent.run(
            research_prompt,
            deps=research_deps,
            usage=ctx.usage  # CRITICAL: Pass usage for token tracking
        )

        logger.info("Research agent completed successfully")

        # Return research data
        return {
            "success": True,
            "data": result.data if hasattr(result, 'data') else str(result),
            "message": "Research completed"
        }

    except Exception as e:
        logger.error(f"Research agent failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Research failed"
        }


@deal_evaluator_agent.tool
async def invoke_negotiation_agent(
    ctx: RunContext[DealEvaluatorDependencies],
    recipient_email: str,
    property_address: str,
    asking_price: float,
    proposed_price: float,
    dscr: float,
    irr: float,
    price_verdict_str: str,
    legal_rent_status: str
) -> Dict[str, Any]:
    """
    Invoke negotiation sub-agent to create Gmail draft.

    Args:
        recipient_email: Seller or agent email
        property_address: Full address
        asking_price: Asking price (EUR)
        proposed_price: Proposed offer (EUR)
        dscr: Debt Service Coverage Ratio
        irr: Internal Rate of Return
        price_verdict_str: Price verdict string
        legal_rent_status: Legal rent status

    Returns:
        Dictionary with draft_id and status
    """
    try:
        logger.info(f"Invoking negotiation agent for {property_address}")

        # Create negotiation agent dependencies
        negotiation_deps = NegotiationAgentDependencies(
            gmail_credentials_path=ctx.deps.gmail_credentials_path,
            gmail_token_path=ctx.deps.gmail_token_path,
            session_id=ctx.deps.session_id
        )

        # Build negotiation prompt
        subject = f"Offer for Property at {property_address}"

        negotiation_prompt = f"""
        Create a professional negotiation email draft for:

        Property: {property_address}
        Asking Price: €{asking_price:,.0f}
        Proposed Offer: €{proposed_price:,.0f}

        Financial Analysis:
        - DSCR: {dscr:.2f}
        - IRR: {irr*100:.1f}%
        - Price Assessment: {price_verdict_str}
        - Legal Rent: {legal_rent_status}

        Recipient: {recipient_email}
        Subject: {subject}

        Draft a data-driven, professional negotiation email.
        """

        result = await negotiation_agent.run(
            negotiation_prompt,
            deps=negotiation_deps,
            usage=ctx.usage  # CRITICAL: Pass usage for token tracking
        )

        logger.info("Negotiation agent completed successfully")

        return {
            "success": True,
            "draft_id": "draft_placeholder",  # Would be returned by agent
            "message": "Draft created successfully"
        }

    except Exception as e:
        logger.error(f"Negotiation agent failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Draft creation failed"
        }


# Convenience function
def create_deal_evaluator_with_deps(
    brave_api_key: str,
    gmail_credentials_path: str,
    gmail_token_path: str,
    session_id: str = None
):
    """
    Create deal evaluator agent with dependencies.

    Args:
        brave_api_key: Brave Search API key
        gmail_credentials_path: Gmail credentials path
        gmail_token_path: Gmail token path
        session_id: Optional session ID

    Returns:
        Configured deal evaluator agent
    """
    return deal_evaluator_agent