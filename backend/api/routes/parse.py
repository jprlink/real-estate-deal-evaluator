"""
PDF parsing API endpoints.
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from backend.parsers.listing import parse_listing_html, normalize_listing_data
from typing import Optional, Dict, Any
import logging


def get_city_from_postal_code(postal_code: str) -> str:
    """
    Infer city name from French postal code.

    Returns the most common city name associated with the postal code,
    not the department name.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        str: City name or empty string if unknown
    """
    if not postal_code or len(postal_code) != 5:
        return ""

    # For Paris arrondissements (750XX)
    if postal_code.startswith("750"):
        return "Paris"

    # Major cities with direct mapping
    dept = postal_code[:2]

    # Île-de-France region - map to major cities
    idf_cities = {
        "92": {  # Hauts-de-Seine
            "920": "Nanterre", "921": "Neuilly-sur-Seine", "922": "Boulogne-Billancourt",
            "923": "Levallois-Perret", "924": "Clichy", "925": "Colombes", "926": "Courbevoie",
            "927": "Asnières-sur-Seine", "928": "Issy-les-Moulineaux", "929": "Rueil-Malmaison"
        },
        "93": {  # Seine-Saint-Denis
            "930": "Bobigny", "931": "Saint-Denis", "932": "Montreuil", "933": "Aubervilliers",
            "934": "Pantin", "935": "Bondy", "936": "Noisy-le-Sec"
        },
        "94": {  # Val-de-Marne
            "940": "Créteil", "941": "Vitry-sur-Seine", "942": "Ivry-sur-Seine",
            "943": "Maisons-Alfort", "944": "Saint-Mandé", "945": "Vincennes"
        },
        "91": {  # Essonne
            "910": "Évry", "911": "Corbeil-Essonnes", "912": "Massy", "913": "Palaiseau"
        },
        "78": {  # Yvelines
            "780": "Versailles", "781": "Saint-Germain-en-Laye", "782": "Sartrouville"
        },
        "95": {  # Val-d'Oise
            "950": "Cergy", "951": "Argenteuil", "952": "Sarcelles", "953": "Pontoise"
        },
        "77": {  # Seine-et-Marne
            "770": "Melun", "771": "Meaux", "772": "Chelles", "773": "Fontainebleau"
        }
    }

    # Check for specific city match in Île-de-France
    if dept in idf_cities:
        prefix = postal_code[:3]
        if prefix in idf_cities[dept]:
            return idf_cities[dept][prefix]
        # Return first major city in department if no specific match
        return next(iter(idf_cities[dept].values()))

    # Major French cities outside Paris region
    major_cities = {
        "13": "Marseille",
        "69": "Lyon",
        "31": "Toulouse",
        "33": "Bordeaux",
        "59": "Lille",
        "44": "Nantes",
        "67": "Strasbourg",
        "35": "Rennes",
        "34": "Montpellier",
        "06": "Nice",
        "76": "Rouen",
        "44": "Nantes",
        "21": "Dijon",
        "63": "Clermont-Ferrand",
        "83": "Toulon",
        "38": "Grenoble",
        "49": "Angers",
        "54": "Nancy",
        "57": "Metz",
        "29": "Brest",
        "87": "Limoges",
        "25": "Besançon",
        "45": "Orléans",
        "68": "Mulhouse",
        "62": "Calais",
        "80": "Amiens"
    }

    return major_cities.get(dept, "")


def calculate_notary_fees(price: float) -> float:
    """Calculate estimated notary fees (frais de notaire) for property purchase."""
    # Standard rates for old properties (logement ancien): ~7-8%
    # For new properties (logement neuf): ~2-3%
    # Using 7.5% as average for old properties
    return price * 0.075


def calculate_financing_defaults(price: float, monthly_rent: float = None) -> Dict[str, Any]:
    """Calculate smart financing defaults based on price."""
    # Standard assumptions:
    # - Down payment: 20% (minimum for investment properties)
    # - Interest rate: 3.5% (current market average)
    # - Loan term: 20 years (standard for investment)
    # - Monthly rent: estimate 3-4% gross yield if not provided

    down_payment = price * 0.20
    loan_amount = price * 0.80
    annual_rate = 0.035
    loan_term = 20

    if monthly_rent is None:
        # Estimate rent based on 3.5% gross yield
        annual_rent = price * 0.035
        monthly_rent = annual_rent / 12

    return {
        "down_payment": round(down_payment, 2),
        "loan_amount": round(loan_amount, 2),
        "annual_rate": annual_rate,
        "loan_term": loan_term,
        "monthly_rent": round(monthly_rent, 2) if monthly_rent else None
    }

router = APIRouter()
logger = logging.getLogger(__name__)


class ParseResponse(BaseModel):
    address: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    price: Optional[float] = None
    surface: Optional[float] = None
    rooms: Optional[int] = None
    bedrooms: Optional[int] = None
    floor: Optional[int] = None
    dpe: Optional[str] = None
    copropriety_fees: Optional[float] = None
    notary_fees: Optional[float] = None
    down_payment: Optional[float] = None
    loan_amount: Optional[float] = None
    annual_rate: Optional[float] = None
    loan_term: Optional[int] = None
    monthly_rent: Optional[float] = None
    success: bool
    message: str


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
            # Calculate additional fields
            city = get_city_from_postal_code(postal_code) if postal_code else None
            notary_fees = calculate_notary_fees(normalized["price"]) if normalized.get("price") else None
            financing = calculate_financing_defaults(
                normalized["price"],
                normalized.get("monthly_rent")
            ) if normalized.get("price") else {}

            # Use city name for location field (not quartier)
            location = city or address_str

            return ParseResponse(
                success=True,
                message=f"Successfully parsed {file.filename}! Extracted property details and calculated smart defaults. Please review.",
                address=location,  # This becomes the Location field value
                postal_code=postal_code,
                city=city,
                price=normalized.get("price"),
                surface=normalized.get("surface"),
                rooms=normalized.get("rooms"),
                bedrooms=normalized.get("bedrooms"),
                floor=normalized.get("floor"),
                dpe=normalized.get("dpe"),
                copropriety_fees=normalized.get("copropriety_fees"),
                notary_fees=notary_fees,
                down_payment=financing.get("down_payment"),
                loan_amount=financing.get("loan_amount"),
                annual_rate=financing.get("annual_rate"),
                loan_term=financing.get("loan_term"),
                monthly_rent=financing.get("monthly_rent")
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
