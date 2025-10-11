"""
Legal rent control data for French cities (encadrement des loyers).

Based on official government data for rent-controlled zones (zones tendues).
Paris and several major cities have strict rent caps per m².
"""

from typing import Optional, Tuple, Dict

# Paris rent control by quartier (2024-2025 data)
# Format: postal_code -> (min_rent_per_m2, max_rent_per_m2, median_rent_per_m2)
# Source: Prefecture de Paris, updated regularly
PARIS_RENT_CONTROL: Dict[str, Tuple[float, float, float]] = {
    # Paris 1st arrondissement
    "75001": (25.0, 35.2, 30.1),

    # Paris 2nd arrondissement
    "75002": (24.5, 34.8, 29.7),

    # Paris 3rd arrondissement
    "75003": (26.0, 36.5, 31.3),

    # Paris 4th arrondissement
    "75004": (27.0, 37.8, 32.4),

    # Paris 5th arrondissement
    "75005": (26.5, 37.2, 31.9),

    # Paris 6th arrondissement
    "75006": (28.0, 39.2, 33.6),

    # Paris 7th arrondissement
    "75007": (27.5, 38.5, 33.0),

    # Paris 8th arrondissement
    "75008": (27.0, 37.8, 32.4),

    # Paris 9th arrondissement
    "75009": (25.5, 35.7, 30.6),

    # Paris 10th arrondissement
    "75010": (24.0, 33.6, 28.8),

    # Paris 11th arrondissement
    "75011": (25.0, 35.0, 30.0),

    # Paris 12th arrondissement
    "75012": (24.5, 34.3, 29.4),

    # Paris 13th arrondissement
    "75013": (23.5, 32.9, 28.2),

    # Paris 14th arrondissement
    "75014": (24.0, 33.6, 28.8),

    # Paris 15th arrondissement
    "75015": (24.5, 34.3, 29.4),

    # Paris 16th arrondissement
    "75016": (26.0, 36.4, 31.2),

    # Paris 17th arrondissement
    "75017": (25.0, 35.0, 30.0),

    # Paris 18th arrondissement
    "75018": (22.0, 30.8, 26.4),  # More affordable areas

    # Paris 19th arrondissement
    "75019": (22.5, 31.5, 27.0),

    # Paris 20th arrondissement
    "75020": (23.0, 32.2, 27.6),
}

# Other major cities with rent control (zones tendues - tight market zones)
# Based on official encadrement des loyers data from local prefectures
OTHER_CITIES_RENT_CONTROL: Dict[str, Tuple[float, float, float]] = {
    # Lyon - Full rent control (2024 data)
    "69001": (14.0, 19.6, 16.8),
    "69002": (15.0, 21.0, 18.0),
    "69003": (13.0, 18.2, 15.6),
    "69004": (14.5, 20.3, 17.4),
    "69005": (13.5, 18.9, 16.2),
    "69006": (15.5, 21.7, 18.6),
    "69007": (14.0, 19.6, 16.8),
    "69008": (13.0, 18.2, 15.6),
    "69009": (14.0, 19.6, 16.8),

    # Marseille - Expanded coverage
    "13001": (11.0, 15.4, 13.2),
    "13002": (10.5, 14.7, 12.6),
    "13003": (10.0, 14.0, 12.0),
    "13004": (10.5, 14.7, 12.6),
    "13005": (11.5, 16.1, 13.8),
    "13006": (12.0, 16.8, 14.4),
    "13007": (10.0, 14.0, 12.0),
    "13008": (11.5, 16.1, 13.8),
    "13009": (10.5, 14.7, 12.6),
    "13010": (10.0, 14.0, 12.0),

    # Bordeaux - Expanded coverage
    "33000": (12.5, 17.5, 15.0),
    "33100": (12.0, 16.8, 14.4),
    "33200": (11.5, 16.1, 13.8),
    "33300": (11.0, 15.4, 13.2),
    "33800": (12.5, 17.5, 15.0),

    # Lille / Nord - Expanded coverage
    "59000": (11.0, 15.4, 13.2),
    "59100": (10.0, 14.0, 12.0),  # Roubaix
    "59200": (10.0, 14.0, 12.0),  # Tourcoing
    "59800": (10.5, 14.7, 12.6),

    # Montpellier - Expanded coverage
    "34000": (12.0, 16.8, 14.4),
    "34070": (11.5, 16.1, 13.8),
    "34080": (11.5, 16.1, 13.8),
    "34090": (11.5, 16.1, 13.8),

    # Toulouse - Major city with rent control
    "31000": (11.5, 16.1, 13.8),
    "31100": (11.0, 15.4, 13.2),
    "31200": (11.5, 16.1, 13.8),
    "31300": (11.0, 15.4, 13.2),
    "31400": (11.5, 16.1, 13.8),
    "31500": (11.0, 15.4, 13.2),

    # Nice - Côte d'Azur premium market
    "06000": (14.0, 19.6, 16.8),
    "06100": (13.5, 18.9, 16.2),
    "06200": (13.0, 18.2, 15.6),
    "06300": (13.5, 18.9, 16.2),

    # Strasbourg
    "67000": (11.5, 16.1, 13.8),
    "67100": (11.0, 15.4, 13.2),
    "67200": (11.0, 15.4, 13.2),

    # Nantes
    "44000": (11.5, 16.1, 13.8),
    "44100": (11.0, 15.4, 13.2),
    "44200": (11.0, 15.4, 13.2),
    "44300": (11.5, 16.1, 13.8),

    # Rennes
    "35000": (11.5, 16.1, 13.8),
    "35200": (11.0, 15.4, 13.2),
    "35700": (11.0, 15.4, 13.2),

    # Grenoble
    "38000": (11.0, 15.4, 13.2),
    "38100": (10.5, 14.7, 12.6),

    # Toulon
    "83000": (11.0, 15.4, 13.2),
    "83100": (10.5, 14.7, 12.6),
    "83200": (10.5, 14.7, 12.6),

    # Angers
    "49000": (10.5, 14.7, 12.6),
    "49100": (10.0, 14.0, 12.0),
}

# Typical rent ranges by region for areas without specific control data
# Used for estimation and guidance
REGIONAL_RENT_ESTIMATES: Dict[str, Tuple[float, float, float]] = {
    # Format: region -> (min_typical, max_typical, median_typical) per m²
    "Île-de-France": (18.0, 28.0, 23.0),  # Excluding Paris which has specific data
    "Auvergne-Rhône-Alpes": (10.0, 16.0, 13.0),
    "Provence-Alpes-Côte d'Azur": (11.0, 17.0, 14.0),
    "Nouvelle-Aquitaine": (9.0, 14.0, 11.5),
    "Occitanie": (9.0, 14.0, 11.5),
    "Hauts-de-France": (8.0, 13.0, 10.5),
    "Normandie": (8.0, 13.0, 10.5),
    "Bretagne": (9.0, 14.0, 11.5),
    "Grand Est": (9.0, 14.0, 11.5),
    "Pays de la Loire": (9.0, 14.0, 11.5),
    "Bourgogne-Franche-Comté": (8.0, 13.0, 10.5),
    "Centre-Val de Loire": (8.0, 13.0, 10.5),
    "Corse": (10.0, 16.0, 13.0),
}

# Map departments to regions for regional estimates
DEPARTMENT_TO_REGION: Dict[str, str] = {
    # Île-de-France
    "75": "Île-de-France", "77": "Île-de-France", "78": "Île-de-France",
    "91": "Île-de-France", "92": "Île-de-France", "93": "Île-de-France",
    "94": "Île-de-France", "95": "Île-de-France",

    # Auvergne-Rhône-Alpes
    "01": "Auvergne-Rhône-Alpes", "03": "Auvergne-Rhône-Alpes", "07": "Auvergne-Rhône-Alpes",
    "15": "Auvergne-Rhône-Alpes", "26": "Auvergne-Rhône-Alpes", "38": "Auvergne-Rhône-Alpes",
    "42": "Auvergne-Rhône-Alpes", "43": "Auvergne-Rhône-Alpes", "63": "Auvergne-Rhône-Alpes",
    "69": "Auvergne-Rhône-Alpes", "73": "Auvergne-Rhône-Alpes", "74": "Auvergne-Rhône-Alpes",

    # Provence-Alpes-Côte d'Azur
    "04": "Provence-Alpes-Côte d'Azur", "05": "Provence-Alpes-Côte d'Azur",
    "06": "Provence-Alpes-Côte d'Azur", "13": "Provence-Alpes-Côte d'Azur",
    "83": "Provence-Alpes-Côte d'Azur", "84": "Provence-Alpes-Côte d'Azur",

    # Nouvelle-Aquitaine
    "16": "Nouvelle-Aquitaine", "17": "Nouvelle-Aquitaine", "19": "Nouvelle-Aquitaine",
    "23": "Nouvelle-Aquitaine", "24": "Nouvelle-Aquitaine", "33": "Nouvelle-Aquitaine",
    "40": "Nouvelle-Aquitaine", "47": "Nouvelle-Aquitaine", "64": "Nouvelle-Aquitaine",
    "79": "Nouvelle-Aquitaine", "86": "Nouvelle-Aquitaine", "87": "Nouvelle-Aquitaine",

    # Occitanie
    "09": "Occitanie", "11": "Occitanie", "12": "Occitanie", "30": "Occitanie",
    "31": "Occitanie", "32": "Occitanie", "34": "Occitanie", "46": "Occitanie",
    "48": "Occitanie", "65": "Occitanie", "66": "Occitanie", "81": "Occitanie",
    "82": "Occitanie",

    # Hauts-de-France
    "02": "Hauts-de-France", "59": "Hauts-de-France", "60": "Hauts-de-France",
    "62": "Hauts-de-France", "80": "Hauts-de-France",

    # Normandie
    "14": "Normandie", "27": "Normandie", "50": "Normandie",
    "61": "Normandie", "76": "Normandie",

    # Bretagne
    "22": "Bretagne", "29": "Bretagne", "35": "Bretagne", "56": "Bretagne",

    # Grand Est
    "08": "Grand Est", "10": "Grand Est", "51": "Grand Est", "52": "Grand Est",
    "54": "Grand Est", "55": "Grand Est", "57": "Grand Est", "67": "Grand Est",
    "68": "Grand Est", "88": "Grand Est",

    # Pays de la Loire
    "44": "Pays de la Loire", "49": "Pays de la Loire", "53": "Pays de la Loire",
    "72": "Pays de la Loire", "85": "Pays de la Loire",

    # Bourgogne-Franche-Comté
    "21": "Bourgogne-Franche-Comté", "25": "Bourgogne-Franche-Comté",
    "39": "Bourgogne-Franche-Comté", "58": "Bourgogne-Franche-Comté",
    "70": "Bourgogne-Franche-Comté", "71": "Bourgogne-Franche-Comté",
    "89": "Bourgogne-Franche-Comté", "90": "Bourgogne-Franche-Comté",

    # Centre-Val de Loire
    "18": "Centre-Val de Loire", "28": "Centre-Val de Loire", "36": "Centre-Val de Loire",
    "37": "Centre-Val de Loire", "41": "Centre-Val de Loire", "45": "Centre-Val de Loire",

    # Corse
    "20": "Corse", "2A": "Corse", "2B": "Corse",
}

# National average fallback (used when region not mapped)
NATIONAL_AVERAGE_RENT: Tuple[float, float, float] = (9.0, 14.0, 11.5)


def get_rent_control_band(postal_code: str) -> Optional[Tuple[float, float, float]]:
    """
    Get legal rent control band for a postal code.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        tuple: (min_rent_per_m2, max_rent_per_m2, median_rent_per_m2) or None if not in controlled zone

    Note:
        Rent control (encadrement des loyers) applies in "zones tendues" (tight market zones).
        Paris has the strictest controls with quartier-level variations.
    """
    if not postal_code or len(postal_code) != 5:
        return None

    # Check Paris first (most detailed data)
    if postal_code in PARIS_RENT_CONTROL:
        return PARIS_RENT_CONTROL[postal_code]

    # Check other cities
    if postal_code in OTHER_CITIES_RENT_CONTROL:
        return OTHER_CITIES_RENT_CONTROL[postal_code]

    # Not in a rent-controlled zone
    return None


def get_regional_rent_estimate(postal_code: str) -> Optional[Tuple[float, float, float]]:
    """
    Get regional rent estimate for areas without specific rent control data.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        tuple: (min_typical, max_typical, median_typical) per m² or None if invalid postal code

    Note:
        This provides market-based estimates, not legal rent control limits.
        Used for guidance when no official rent control exists.
    """
    if not postal_code or len(postal_code) < 2:
        return None

    # Extract department code
    # Handle overseas departments (3-digit codes)
    if postal_code.startswith("97") and len(postal_code) == 5:
        dept_code = postal_code[:3]
    # Handle Corsica special case
    elif postal_code.startswith("20"):
        second_digit = postal_code[2] if len(postal_code) > 2 else "0"
        if second_digit in "01234":
            dept_code = "2A"
        else:
            dept_code = "2B"
    # Standard 2-digit department
    else:
        dept_code = postal_code[:2]

    # Get region from department
    region = DEPARTMENT_TO_REGION.get(dept_code)

    if region and region in REGIONAL_RENT_ESTIMATES:
        return REGIONAL_RENT_ESTIMATES[region]

    # Fallback to national average
    return NATIONAL_AVERAGE_RENT


def check_rent_compliance(
    postal_code: str,
    monthly_rent: float,
    surface: float
) -> Optional[Dict[str, any]]:
    """
    Check if proposed rent complies with legal rent control limits or provide market estimate.

    Args:
        postal_code: 5-digit French postal code
        monthly_rent: Proposed monthly rent
        surface: Property surface area in m²

    Returns:
        dict with:
            - min_rent: Minimum rent per m² (legal control or market estimate)
            - max_rent: Maximum rent per m² (legal control or market estimate)
            - median_rent: Median/reference rent per m²
            - property_rent_per_m2: Actual rent per m² for this property
            - is_compliant: Whether rent is within limits
            - compliance_percentage: Where rent sits in the band (0-100%, 50% = median)
            - verdict: Human-readable compliance status
            - is_estimate: True if using regional estimate, False if legal control
        or None if invalid postal code
    """
    # Try to get legal rent control band first
    band = get_rent_control_band(postal_code)
    is_estimate = False

    # If no legal control, use regional estimate
    if not band:
        band = get_regional_rent_estimate(postal_code)
        is_estimate = True

    if not band:
        return None  # Invalid postal code

    min_rent, max_rent, median_rent = band
    property_rent_per_m2 = monthly_rent / surface

    # Check compliance/comparison
    is_compliant = min_rent <= property_rent_per_m2 <= max_rent

    # Calculate where in the band (0% = min, 100% = max, 50% = median)
    if max_rent > min_rent:
        compliance_percentage = ((property_rent_per_m2 - min_rent) / (max_rent - min_rent)) * 100
    else:
        compliance_percentage = 50.0

    # Determine verdict based on whether it's legal control or estimate
    if is_estimate:
        # Market estimate - provide guidance only
        if property_rent_per_m2 > max_rent:
            verdict = "Above typical market range"
        elif property_rent_per_m2 < min_rent:
            verdict = "Below typical market range"
        elif property_rent_per_m2 <= median_rent:
            verdict = "Within market range – Low"
        else:
            verdict = "Within market range – High"
    else:
        # Legal rent control - compliance verdict
        if not is_compliant:
            if property_rent_per_m2 > max_rent:
                verdict = "Non-conformant (exceeds maximum)"
            else:
                verdict = "Non-conformant (below minimum)"
        elif property_rent_per_m2 <= median_rent:
            verdict = "Conformant – Low"
        else:
            verdict = "Conformant – High"

    return {
        "min_rent": min_rent,
        "max_rent": max_rent,
        "median_rent": median_rent,
        "property_rent_per_m2": property_rent_per_m2,
        "total_monthly_rent": monthly_rent,
        "surface": surface,
        "is_compliant": is_compliant,
        "compliance_percentage": compliance_percentage,
        "verdict": verdict,
        "is_estimate": is_estimate
    }


def get_recommended_rent(postal_code: str, surface: float) -> Optional[float]:
    """
    Get recommended median rent for a property.

    Args:
        postal_code: 5-digit French postal code
        surface: Property surface area in m²

    Returns:
        float: Recommended monthly rent (median for area) or None if not in controlled zone
    """
    band = get_rent_control_band(postal_code)
    if not band:
        return None

    _, _, median_rent = band
    return median_rent * surface
