"""
Real estate appreciation rates by department and postal code.

Based on market data from Notaires de France and French government statistics (2024-2025).
Rates represent historical annual appreciation and forward-looking estimates.
"""

from typing import Dict, Optional

# Annual appreciation rates by department (%)
# Based on 2024-2025 market data
# Negative values represent price corrections
# Source: Notaires de France, Q4 2024 / Q1 2025 data
DEPARTMENT_APPRECIATION_RATES: Dict[str, float] = {
    # Île-de-France (Paris Region)
    "75": -2.9,   # Paris - significant correction in 2024, stabilizing 2025
    "92": -3.0,   # Hauts-de-Seine - inner suburbs correction
    "93": -3.2,   # Seine-Saint-Denis - outer suburbs correction
    "94": -3.0,   # Val-de-Marne - moderate correction
    "91": -3.6,   # Essonne - larger correction in outer areas
    "78": -5.0,   # Yvelines - houses declining more than apartments
    "95": -3.6,   # Val-d'Oise - outer region correction
    "77": -5.0,   # Seine-et-Marne - houses declining significantly

    # Major provincial cities (generally more stable than Paris)
    "13": -0.5,   # Bouches-du-Rhône (Marseille) - mild correction
    "69": -1.0,   # Rhône (Lyon) - slight correction
    "31": 0.5,    # Haute-Garonne (Toulouse) - resilient market
    "33": -0.8,   # Gironde (Bordeaux) - mild correction
    "59": -1.2,   # Nord (Lille) - moderate correction
    "44": 0.3,    # Loire-Atlantique (Nantes) - stable/growing
    "67": -0.5,   # Bas-Rhin (Strasbourg) - stable
    "35": 0.8,    # Ille-et-Vilaine (Rennes) - growing market
    "34": 0.2,    # Hérault (Montpellier) - stable
    "06": 0.0,    # Alpes-Maritimes (Nice) - remarkably stable in 2024
    "76": -1.5,   # Seine-Maritime (Rouen) - correction
    "21": -1.0,   # Côte-d'Or (Dijon) - mild correction
    "63": -1.2,   # Puy-de-Dôme (Clermont-Ferrand) - moderate correction
    "83": -0.3,   # Var (Toulon) - mild correction
    "38": -0.7,   # Isère (Grenoble) - slight correction
    "49": -0.9,   # Maine-et-Loire (Angers) - mild correction
    "54": -1.3,   # Meurthe-et-Moselle (Nancy) - correction
    "57": -1.4,   # Moselle (Metz) - correction
    "29": -0.8,   # Finistère (Brest) - mild correction
    "87": -1.5,   # Haute-Vienne (Limoges) - correction
    "25": -1.1,   # Doubs (Besançon) - correction
    "45": -1.0,   # Loiret (Orléans) - mild correction
    "68": -1.2,   # Haut-Rhin (Mulhouse) - correction
    "62": -1.8,   # Pas-de-Calais (Calais) - larger correction
    "80": -1.6,   # Somme (Amiens) - correction

    # Other departments (estimated based on regional trends)
    "01": -1.0, "02": -1.5, "03": -1.3, "04": -0.5, "05": -0.7,
    "07": -0.8, "08": -1.7, "09": -0.9, "10": -1.4, "11": -0.6,
    "12": -1.0, "14": -1.2, "15": -1.1, "16": -1.3, "17": 0.2,
    "18": -1.5, "19": -1.2, "22": -0.5, "23": -1.6, "24": -0.9,
    "26": -0.8, "27": -2.5, "28": -1.8, "30": -0.4, "32": -0.7,
    "36": -1.7, "37": -0.8, "39": -1.1, "40": 0.1, "41": -1.3,
    "42": -1.0, "43": -1.2, "46": -0.9, "47": -1.0, "48": -1.1,
    "50": -1.3, "51": -1.5, "52": -1.6, "53": -1.2, "55": -1.7,
    "56": -0.3, "58": -1.6, "60": -2.8, "61": -1.4, "64": 0.3,
    "65": -0.8, "66": -0.2, "70": -1.5, "71": -1.1, "72": -1.0,
    "73": 0.0, "74": 0.5, "79": -1.0, "81": -0.7, "82": -1.0,
    "84": -0.5, "85": 0.4, "86": -1.3, "88": -1.4, "89": -1.5,
    "90": -1.3,
}

# Forward-looking adjustment for 2025+
# Market expected to stabilize with slight growth (+0.1% to +1% nationally)
FORWARD_ADJUSTMENT = 1.5  # Add this to historical rates for forward projections


def get_appreciation_rate(postal_code: Optional[str] = None,
                         department: Optional[str] = None,
                         forward_looking: bool = True) -> float:
    """
    Get annual real estate appreciation rate for a location.

    Args:
        postal_code: 5-digit French postal code (preferred)
        department: 2-digit department code (fallback)
        forward_looking: If True, applies forward adjustment for future years

    Returns:
        float: Annual appreciation rate as decimal (e.g., 0.02 for 2%)
               Returns 0.5% (0.005) as conservative default if not found

    Examples:
        >>> get_appreciation_rate("75001")  # Paris
        -0.014  # -1.4% (after forward adjustment from -2.9%)
        >>> get_appreciation_rate("06000")  # Nice
        0.015  # 1.5% (stable market + forward adjustment)
        >>> get_appreciation_rate(department="35")  # Rennes
        0.023  # 2.3% (growing market + forward adjustment)
    """
    # Extract department from postal code
    if postal_code and len(postal_code) == 5:
        department = postal_code[:2]

    # Get base rate
    base_rate = DEPARTMENT_APPRECIATION_RATES.get(department, 0.5)  # 0.5% default

    # Apply forward-looking adjustment if requested
    if forward_looking:
        adjusted_rate = base_rate + FORWARD_ADJUSTMENT
    else:
        adjusted_rate = base_rate

    # Convert from percentage to decimal
    return adjusted_rate / 100.0


def get_appreciation_rate_display(postal_code: Optional[str] = None,
                                  department: Optional[str] = None,
                                  forward_looking: bool = True) -> str:
    """
    Get appreciation rate formatted for display.

    Args:
        postal_code: 5-digit French postal code
        department: 2-digit department code
        forward_looking: If True, uses forward-looking rate

    Returns:
        str: Formatted rate (e.g., "+2.3%" or "-1.5%")
    """
    rate = get_appreciation_rate(postal_code, department, forward_looking)
    percentage = rate * 100
    sign = "+" if percentage >= 0 else ""
    return f"{sign}{percentage:.1f}%"


def get_appreciation_source() -> str:
    """
    Get data source information for appreciation rates.

    Returns:
        str: Source description
    """
    return ("Based on Notaires de France Q4 2024 / Q1 2025 market data. "
            "Forward projections include stabilization adjustment (+1.5%). "
            "Actual rates may vary by neighborhood and property type.")
