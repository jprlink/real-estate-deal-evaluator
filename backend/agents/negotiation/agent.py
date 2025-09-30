"""
Negotiation email agent for drafting Gmail negotiations.
"""

import logging
from typing import Dict, Any

from pydantic_ai import Agent, RunContext
from dataclasses import dataclass

from backend.agents.providers import get_llm_model
from backend.agents.negotiation.prompts import NEGOTIATION_SYSTEM_PROMPT
from backend.agents.negotiation import tools

logger = logging.getLogger(__name__)


@dataclass
class NegotiationAgentDependencies:
    """Dependencies for the negotiation agent."""
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: str = None


# Create negotiation agent (NO result_type - default to string)
negotiation_agent = Agent(
    get_llm_model(),
    deps_type=NegotiationAgentDependencies,
    system_prompt=NEGOTIATION_SYSTEM_PROMPT
)


@negotiation_agent.tool
async def create_negotiation_email_draft(
    ctx: RunContext[NegotiationAgentDependencies],
    recipient_email: str,
    subject: str,
    property_address: str,
    asking_price: float,
    proposed_price: float,
    dscr: float,
    irr: float,
    price_verdict: str,
    legal_rent_status: str,
    comparable_sales: str = None,
    additional_context: str = None
) -> Dict[str, Any]:
    """
    Create a negotiation email draft in Gmail.

    Args:
        recipient_email: Seller or agent email address
        subject: Email subject line
        property_address: Full property address
        asking_price: Seller's asking price (EUR)
        proposed_price: Your proposed offer price (EUR)
        dscr: Debt Service Coverage Ratio
        irr: Internal Rate of Return (as decimal, e.g., 0.085)
        price_verdict: Price verdict (Under-priced/Average/Overpriced)
        legal_rent_status: Legal rent compliance status
        comparable_sales: Optional text describing comparable sales
        additional_context: Optional additional negotiation context

    Returns:
        Dictionary with draft_id and success status
    """
    try:
        # Calculate discount
        discount_pct = ((asking_price - proposed_price) / asking_price) * 100

        # Build email body with financial analysis
        body = f"""Dear Property Owner / Agent,

I am writing to express my interest in the property located at {property_address}, currently listed at €{asking_price:,.0f}.

After conducting thorough market research and financial analysis, I would like to present an offer of €{proposed_price:,.0f} (representing a {discount_pct:.1f}% adjustment from the asking price).

**Market Analysis:**
{comparable_sales if comparable_sales else "Based on recent comparable sales in the area, the property appears to be positioned in line with market rates."}

**Financial Analysis:**
- Debt Service Coverage Ratio (DSCR): {dscr:.2f}
- Internal Rate of Return (IRR): {irr*100:.1f}%
- Price Assessment: {price_verdict}
- Legal Rent Status: {legal_rent_status}

The proposed price reflects current market conditions and ensures a sustainable investment return while offering you a fair value for the property.

{additional_context if additional_context else ""}

I am prepared to move forward quickly with this transaction and would appreciate the opportunity to discuss this offer with you. I am flexible on closing timeline and other terms that may be important to you.

Please let me know your thoughts on this proposal. I am available for a call or meeting at your convenience.

Best regards,
[Your Name]
[Your Contact Information]

---
This draft was prepared with data-driven analysis. Please review and customize before sending.
"""

        # Create Gmail draft
        draft_id = await tools.create_gmail_draft_tool(
            credentials_path=ctx.deps.gmail_credentials_path,
            token_path=ctx.deps.gmail_token_path,
            to=recipient_email,
            subject=subject,
            body=body
        )

        logger.info(f"Created negotiation draft {draft_id} for {property_address}")

        return {
            "success": True,
            "draft_id": draft_id,
            "recipient": recipient_email,
            "subject": subject,
            "property_address": property_address,
            "proposed_price": proposed_price,
            "discount_percent": discount_pct
        }

    except Exception as e:
        logger.error(f"Failed to create negotiation draft: {e}")
        return {
            "success": False,
            "error": str(e),
            "recipient": recipient_email,
            "property_address": property_address
        }


# Convenience function
def create_negotiation_agent_with_deps(
    gmail_credentials_path: str,
    gmail_token_path: str,
    session_id: str = None
):
    """
    Create negotiation agent with dependencies.

    Args:
        gmail_credentials_path: Path to Gmail credentials
        gmail_token_path: Path to Gmail token
        session_id: Optional session ID

    Returns:
        Configured negotiation agent
    """
    return negotiation_agent