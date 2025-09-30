"""
Shared dependency dataclasses for PydanticAI agents.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResearchAgentDependencies:
    """Dependencies for the research agent."""
    brave_api_key: str
    session_id: Optional[str] = None


@dataclass
class NegotiationAgentDependencies:
    """Dependencies for the negotiation email agent."""
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None


@dataclass
class DealEvaluatorDependencies:
    """Dependencies for the primary deal evaluator agent."""
    brave_api_key: str
    gmail_credentials_path: str
    gmail_token_path: str
    session_id: Optional[str] = None