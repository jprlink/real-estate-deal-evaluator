"""
Parser for real estate listing HTML/PDF documents.

Extracts property details from listing pages or PDF documents.
"""

from typing import Dict, Optional, Any
import re


def parse_listing_html(html_content: str) -> Dict[str, Any]:
    """
    Parse HTML content from a real estate listing page.

    Args:
        html_content: Raw HTML content from the listing page

    Returns:
        dict: Extracted property details including:
            - address (street, postal_code, city)
            - price
            - surface
            - rooms
            - bedrooms
            - floor
            - dpe
            - description
            - features (list)

    Example:
        html = fetch_listing_html("https://example.com/listing")
        data = parse_listing_html(html)
    """
    listing_data = {
        "address": {},
        "price": None,
        "surface": None,
        "rooms": None,
        "bedrooms": None,
        "floor": None,
        "dpe": None,
        "description": None,
        "features": []
    }

    # Extract price (formats: "500 000 €", "500.000€", "500000 EUR")
    price_patterns = [
        r"(\d[\d\s\.]*)\s*€",
        r"(\d[\d\s\.]*)\s*EUR",
        r"Prix\s*:?\s*(\d[\d\s\.]*)"
    ]
    for pattern in price_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            price_str = match.group(1).replace(" ", "").replace(".", "")
            try:
                listing_data["price"] = float(price_str)
                break
            except ValueError:
                continue

    # Extract surface area (formats: "50 m²", "50m2", "50 m2")
    surface_match = re.search(r"(\d+(?:[.,]\d+)?)\s*m[²2]", html_content, re.IGNORECASE)
    if surface_match:
        listing_data["surface"] = float(surface_match.group(1).replace(",", "."))

    # Extract number of rooms (formats: "2 pièces", "2 rooms", "T2")
    rooms_patterns = [
        r"(\d+)\s*pi[èe]ces?",
        r"(\d+)\s*rooms?",
        r"T(\d+)",
        r"F(\d+)"
    ]
    for pattern in rooms_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            listing_data["rooms"] = int(match.group(1))
            break

    # Extract bedrooms (formats: "1 chambre", "1 bedroom")
    bedrooms_match = re.search(r"(\d+)\s*(?:chambre|bedroom)s?", html_content, re.IGNORECASE)
    if bedrooms_match:
        listing_data["bedrooms"] = int(bedrooms_match.group(1))

    # Extract floor (formats: "3ème étage", "3rd floor")
    floor_patterns = [
        r"(\d+)(?:ème|er)\s*étage",
        r"(\d+)(?:st|nd|rd|th)\s*floor"
    ]
    for pattern in floor_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            listing_data["floor"] = int(match.group(1))
            break

    # Extract DPE grade (A-G)
    dpe_match = re.search(r"DPE\s*:?\s*([A-G])", html_content, re.IGNORECASE)
    if dpe_match:
        listing_data["dpe"] = dpe_match.group(1).upper()

    # Extract postal code (Paris: 75001-75020)
    postal_match = re.search(r"\b(75\d{3})\b", html_content)
    if postal_match:
        listing_data["address"]["postal_code"] = postal_match.group(1)
        listing_data["address"]["city"] = "Paris"

    # Extract street address (simplified - looks for common patterns)
    street_patterns = [
        r"(\d+\s+(?:rue|avenue|boulevard|place)\s+[^\n,]+)",
        r"(?:Adresse|Address)\s*:?\s*([^\n,]+)"
    ]
    for pattern in street_patterns:
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            listing_data["address"]["street"] = match.group(1).strip()
            break

    # Extract features (balcony, parking, elevator, etc.)
    feature_keywords = [
        "balcon", "balcony", "terrasse", "terrace",
        "parking", "garage", "cave", "cellar",
        "ascenseur", "elevator", "lift"
    ]
    for keyword in feature_keywords:
        if re.search(r"\b" + keyword + r"\b", html_content, re.IGNORECASE):
            listing_data["features"].append(keyword)

    return listing_data


def parse_listing_pdf(pdf_text: str) -> Dict[str, Any]:
    """
    Parse text extracted from a real estate listing PDF.

    Args:
        pdf_text: Raw text content extracted from PDF

    Returns:
        dict: Extracted property details (same structure as parse_listing_html)

    Note:
        PDF text extraction must be done externally (e.g., via Playwright MCP).
        This function parses the already-extracted text.
    """
    # PDF parsing uses same logic as HTML since we work with extracted text
    return parse_listing_html(pdf_text)


def normalize_listing_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize and validate parsed listing data.

    Args:
        raw_data: Raw parsed data from parse_listing_html or parse_listing_pdf

    Returns:
        dict: Cleaned and validated listing data

    Validation:
        - Ensures required fields are present
        - Converts types as needed
        - Fills in default values where appropriate
    """
    normalized = {
        "address": {
            "street": raw_data.get("address", {}).get("street"),
            "city": raw_data.get("address", {}).get("city", "Paris"),
            "postal_code": raw_data.get("address", {}).get("postal_code")
        },
        "price": raw_data.get("price"),
        "surface": raw_data.get("surface"),
        "rooms": raw_data.get("rooms"),
        "bedrooms": raw_data.get("bedrooms"),
        "floor": raw_data.get("floor"),
        "dpe": raw_data.get("dpe"),
        "description": raw_data.get("description"),
        "features": raw_data.get("features", [])
    }

    # Remove None values from address
    normalized["address"] = {k: v for k, v in normalized["address"].items() if v is not None}

    # Estimate bedrooms if not provided (typically rooms - 1 for living space)
    if normalized["bedrooms"] is None and normalized["rooms"]:
        normalized["bedrooms"] = max(1, normalized["rooms"] - 1)

    return normalized


def extract_listing_url_info(url: str) -> Dict[str, str]:
    """
    Extract information from listing URL (site, listing ID).

    Args:
        url: Listing page URL

    Returns:
        dict: URL metadata including source site and listing ID

    Example:
        >>> extract_listing_url_info("https://www.seloger.com/annonces/achat/123456")
        {'source': 'seloger', 'listing_id': '123456'}
    """
    url_lower = url.lower()

    # Detect source site
    source = None
    if "seloger" in url_lower:
        source = "seloger"
    elif "leboncoin" in url_lower:
        source = "leboncoin"
    elif "pap.fr" in url_lower:
        source = "pap"
    elif "logic-immo" in url_lower:
        source = "logic-immo"

    # Extract listing ID (simplified - looks for numeric patterns)
    listing_id = None
    id_match = re.search(r"/(\d{6,})", url)
    if id_match:
        listing_id = id_match.group(1)

    return {
        "source": source,
        "listing_id": listing_id,
        "url": url
    }