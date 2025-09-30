"""
PDF and URL parsing API endpoints.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel, HttpUrl
from backend.parsers.listing import parse_listing_html, normalize_listing_data
from typing import Optional, Dict, Any
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class ParseURLRequest(BaseModel):
    url: HttpUrl


class ParseResponse(BaseModel):
    address: Optional[str] = None
    postal_code: Optional[str] = None
    price: Optional[float] = None
    surface: Optional[float] = None
    rooms: Optional[int] = None
    bedrooms: Optional[int] = None
    floor: Optional[int] = None
    dpe: Optional[str] = None
    success: bool
    message: str


@router.post("/parse/url", response_model=ParseResponse)
async def parse_url(request: ParseURLRequest):
    """
    Parse property listing from a URL.

    Note: In production, this would fetch the URL content using requests or playwright.
    For now, returns placeholder data.
    """
    try:
        logger.info(f"Parsing URL: {request.url}")

        # TODO: Implement actual URL fetching and parsing
        # In production:
        # 1. Fetch HTML content from URL
        # 2. Parse with parse_listing_html()
        # 3. Normalize with normalize_listing_data()

        # For now, return sample parsed data
        return ParseResponse(
            success=False,
            message="URL parsing not yet fully implemented. Please use the form to enter property details manually.",
            address=None,
            postal_code=None,
            price=None,
            surface=None,
            rooms=None,
            bedrooms=None,
            floor=None,
            dpe=None
        )

    except Exception as e:
        logger.error(f"Error parsing URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to parse URL: {str(e)}")


@router.post("/parse/pdf", response_model=ParseResponse)
async def parse_pdf(file: UploadFile = File(...)):
    """
    Parse property listing from an uploaded PDF file.

    Extracts property details using regex-based parsing.
    """
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")

        logger.info(f"Parsing PDF: {file.filename}")

        # Read PDF content
        pdf_content = await file.read()

        # Extract text from PDF using pdfplumber
        import pdfplumber
        import io
        import re

        text = ""
        with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        logger.info(f"Extracted {len(text)} characters from PDF")

        if not text.strip():
            return ParseResponse(
                success=False,
                message=f"PDF '{file.filename}' appears to be empty or contains no extractable text.",
                address=None,
                postal_code=None,
                price=None,
                surface=None,
                rooms=None,
                bedrooms=None,
                floor=None,
                dpe=None
            )

        # Parse with existing parser
        parsed = parse_listing_html(text)
        normalized = normalize_listing_data(parsed)

        # Extract address and postal code
        address_str = None
        postal_code = None

        if normalized.get("address"):
            addr = normalized["address"]
            # If address is a dict, convert to string
            if isinstance(addr, dict):
                parts = []
                if addr.get("street"):
                    parts.append(addr["street"])
                if addr.get("city"):
                    parts.append(addr["city"])
                address_str = ", ".join(parts) if parts else None
                postal_code = addr.get("postal_code")
            else:
                # If it's already a string
                address_str = str(addr)
                postal_match = re.search(r"75\d{3}", address_str)
                if postal_match:
                    postal_code = postal_match.group(0)

        # Check if we extracted meaningful data
        has_data = any([
            normalized.get("price"),
            normalized.get("surface"),
            normalized.get("rooms")
        ])

        if has_data:
            return ParseResponse(
                success=True,
                message=f"Successfully parsed {file.filename}! Extracted property details. Please review and complete missing fields.",
                address=address_str,
                postal_code=postal_code,
                price=normalized.get("price"),
                surface=normalized.get("surface"),
                rooms=normalized.get("rooms"),
                bedrooms=normalized.get("bedrooms"),
                floor=normalized.get("floor"),
                dpe=normalized.get("dpe")
            )
        else:
            return ParseResponse(
                success=False,
                message=f"PDF '{file.filename}' was processed but no property details could be extracted. The format may not be recognized. Please enter details manually.",
                address=None,
                postal_code=None,
                price=None,
                surface=None,
                rooms=None,
                bedrooms=None,
                floor=None,
                dpe=None
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error parsing PDF: {str(e)}", exc_info=True)
        return ParseResponse(
            success=False,
            message=f"Error processing PDF: {str(e)}. Please enter details manually.",
            address=None,
            postal_code=None,
            price=None,
            surface=None,
            rooms=None,
            bedrooms=None,
            floor=None,
            dpe=None
        )


@router.post("/parse/text", response_model=ParseResponse)
async def parse_text(html_content: str):
    """
    Parse property listing from raw HTML/text content.
    Uses the existing listing parser.
    """
    try:
        logger.info("Parsing text content")

        # Parse with existing parser
        parsed_data = parse_listing_html(html_content)
        normalized = normalize_listing_data(parsed_data)

        # Extract postal code from address if available
        postal_code = None
        if normalized.get("address"):
            import re
            postal_match = re.search(r"75\d{3}", str(normalized["address"]))
            if postal_match:
                postal_code = postal_match.group(0)

        return ParseResponse(
            success=True,
            message="Property details extracted successfully!",
            address=normalized.get("address"),
            postal_code=postal_code,
            price=normalized.get("price"),
            surface=normalized.get("surface"),
            rooms=normalized.get("rooms"),
            bedrooms=normalized.get("bedrooms"),
            floor=normalized.get("floor"),
            dpe=normalized.get("dpe")
        )

    except Exception as e:
        logger.error(f"Error parsing text: {str(e)}")
        return ParseResponse(
            success=False,
            message=f"Failed to extract property details: {str(e)}",
            address=None,
            postal_code=None,
            price=None,
            surface=None,
            rooms=None,
            bedrooms=None,
            floor=None,
            dpe=None
        )
