"""
Pure tool functions for negotiation agent.
"""

import logging
from backend.integrations import gmail

logger = logging.getLogger(__name__)


async def create_gmail_draft_tool(
    credentials_path: str,
    token_path: str,
    to: str,
    subject: str,
    body: str,
    cc: str = None
) -> str:
    """
    Create a Gmail draft email.

    Args:
        credentials_path: Path to Gmail OAuth credentials.json
        token_path: Path to Gmail OAuth token.json
        to: Recipient email
        subject: Email subject
        body: Email body
        cc: Optional CC recipients

    Returns:
        Draft ID

    Note:
        This calls the Gmail integration stub. Real implementation
        requires OAuth setup and google-api-python-client.
    """
    try:
        draft_id = await gmail.create_draft(
            credentials_path=credentials_path,
            token_path=token_path,
            to=to,
            subject=subject,
            body=body,
            cc=cc
        )
        logger.info(f"Created Gmail draft: {draft_id}")
        return draft_id
    except Exception as e:
        logger.error(f"Error creating Gmail draft: {e}")
        raise