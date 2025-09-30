"""
Parser for Géorisques environmental risk reports (HTML).

Extracts natural and technological risks from Géorisques report pages.
"""

from typing import Dict, List, Any
import re


def parse_georisques_html(html_content: str) -> Dict[str, Any]:
    """
    Parse HTML content from a Géorisques risk report.

    Args:
        html_content: Raw HTML content from Géorisques report page

    Returns:
        dict: Environmental and technological risks including:
            - natural_risks (list of dicts)
            - technological_risks (list of dicts)
            - seismic_zone
            - radon_potential
            - soil_pollution
            - overall_risk_level
            - summary

    Example:
        html = fetch_georisques_report(address)
        risks = parse_georisques_html(html)
    """
    risk_data = {
        "natural_risks": [],
        "technological_risks": [],
        "seismic_zone": None,
        "radon_potential": None,
        "soil_pollution": False,
        "overall_risk_level": "unknown",
        "summary": ""
    }

    # Extract natural risks
    natural_risk_keywords = {
        "inondation": "flood",
        "flood": "flood",
        "mouvement de terrain": "ground_movement",
        "ground movement": "ground_movement",
        "landslide": "ground_movement",
        "sécheresse": "drought",
        "drought": "drought",
        "retrait-gonflement des argiles": "clay_shrinkage",
        "avalanche": "avalanche",
        "feu de forêt": "forest_fire",
        "forest fire": "forest_fire"
    }

    for french_term, english_code in natural_risk_keywords.items():
        if re.search(r"\b" + re.escape(french_term) + r"\b", html_content, re.IGNORECASE):
            # Try to extract risk level (faible, moyen, fort / low, medium, high)
            level = "unknown"
            context_match = re.search(
                rf"{re.escape(french_term)}.*?(faible|moyen|fort|low|medium|high|modéré)",
                html_content,
                re.IGNORECASE | re.DOTALL
            )
            if context_match:
                level_text = context_match.group(1).lower()
                if level_text in ["faible", "low"]:
                    level = "low"
                elif level_text in ["moyen", "medium", "modéré"]:
                    level = "medium"
                elif level_text in ["fort", "high"]:
                    level = "high"

            risk_data["natural_risks"].append({
                "type": english_code,
                "level": level,
                "description": french_term.title()
            })

    # Extract seismic zone (1-5 in France)
    seismic_match = re.search(r"zone\s+sismique\s*:?\s*(\d)", html_content, re.IGNORECASE)
    if seismic_match:
        risk_data["seismic_zone"] = int(seismic_match.group(1))
    else:
        # Try English
        seismic_match = re.search(r"seismic\s+zone\s*:?\s*(\d)", html_content, re.IGNORECASE)
        if seismic_match:
            risk_data["seismic_zone"] = int(seismic_match.group(1))

    # Extract radon potential (1-3 in France)
    radon_match = re.search(r"potentiel\s+radon\s*:?\s*(\d)", html_content, re.IGNORECASE)
    if radon_match:
        risk_data["radon_potential"] = int(radon_match.group(1))
    else:
        # Try English
        radon_match = re.search(r"radon\s+potential\s*:?\s*(\d)", html_content, re.IGNORECASE)
        if radon_match:
            risk_data["radon_potential"] = int(radon_match.group(1))

    # Extract technological risks (ICPE, SEVESO, etc.)
    tech_risk_keywords = {
        "ICPE": "industrial_classified",
        "SEVESO": "seveso",
        "installation classée": "classified_installation",
        "site pollué": "polluted_site",
        "polluted site": "polluted_site"
    }

    for keyword, english_code in tech_risk_keywords.items():
        if re.search(r"\b" + re.escape(keyword) + r"\b", html_content, re.IGNORECASE):
            # Try to extract distance if mentioned
            distance = None
            distance_match = re.search(
                rf"{re.escape(keyword)}.*?(\d+)\s*(?:m|mètres|meters)",
                html_content,
                re.IGNORECASE | re.DOTALL
            )
            if distance_match:
                distance = int(distance_match.group(1))

            risk_data["technological_risks"].append({
                "type": english_code,
                "distance_meters": distance,
                "description": keyword
            })

    # Check for soil pollution indicators
    pollution_keywords = ["pollution des sols", "soil pollution", "site pollué", "polluted site"]
    for keyword in pollution_keywords:
        if keyword in html_content.lower():
            risk_data["soil_pollution"] = True
            break

    # Determine overall risk level based on findings
    risk_data["overall_risk_level"] = _calculate_overall_risk_level(risk_data)

    # Generate summary
    risk_data["summary"] = _generate_risk_summary(risk_data)

    return risk_data


def _calculate_overall_risk_level(risk_data: Dict[str, Any]) -> str:
    """
    Calculate overall risk level based on individual risks.

    Args:
        risk_data: Parsed risk data

    Returns:
        str: "low", "medium", or "high"
    """
    risk_score = 0

    # Natural risks
    for risk in risk_data["natural_risks"]:
        if risk["level"] == "high":
            risk_score += 3
        elif risk["level"] == "medium":
            risk_score += 2
        elif risk["level"] == "low":
            risk_score += 1

    # Seismic zone (1=lowest, 5=highest)
    if risk_data["seismic_zone"]:
        if risk_data["seismic_zone"] >= 4:
            risk_score += 3
        elif risk_data["seismic_zone"] >= 3:
            risk_score += 2
        elif risk_data["seismic_zone"] >= 2:
            risk_score += 1

    # Radon potential (1=lowest, 3=highest)
    if risk_data["radon_potential"]:
        if risk_data["radon_potential"] >= 3:
            risk_score += 2
        elif risk_data["radon_potential"] >= 2:
            risk_score += 1

    # Technological risks
    for risk in risk_data["technological_risks"]:
        if risk.get("distance_meters"):
            if risk["distance_meters"] < 100:
                risk_score += 3
            elif risk["distance_meters"] < 500:
                risk_score += 2
            else:
                risk_score += 1
        else:
            risk_score += 2  # Unknown distance, assume medium risk

    # Soil pollution
    if risk_data["soil_pollution"]:
        risk_score += 3

    # Classify overall risk
    if risk_score >= 8:
        return "high"
    elif risk_score >= 4:
        return "medium"
    else:
        return "low"


def _generate_risk_summary(risk_data: Dict[str, Any]) -> str:
    """
    Generate human-readable summary of risks.

    Args:
        risk_data: Parsed risk data

    Returns:
        str: Summary text
    """
    parts = []

    # Natural risks
    if risk_data["natural_risks"]:
        risk_names = [r["description"] for r in risk_data["natural_risks"]]
        parts.append(f"Natural risks: {', '.join(risk_names)}")

    # Seismic zone
    if risk_data["seismic_zone"]:
        parts.append(f"Seismic zone {risk_data['seismic_zone']}/5")

    # Radon
    if risk_data["radon_potential"]:
        parts.append(f"Radon potential {risk_data['radon_potential']}/3")

    # Technological risks
    if risk_data["technological_risks"]:
        parts.append(f"{len(risk_data['technological_risks'])} technological risk(s)")

    # Soil pollution
    if risk_data["soil_pollution"]:
        parts.append("Soil pollution detected")

    # Overall level
    parts.append(f"Overall risk level: {risk_data['overall_risk_level']}")

    return ". ".join(parts) if parts else "No significant risks identified."


def extract_crime_data(html_content: str, quartier: str) -> Dict[str, Any]:
    """
    Extract crime statistics from data.gouv.fr or similar source.

    Args:
        html_content: Raw HTML from crime statistics page
        quartier: Neighborhood name for context

    Returns:
        dict: Crime statistics including:
            - crime_score (0-100, lower is better)
            - categories (dict of crime types)
            - national_comparison
            - trend

    Note:
        This is a simplified parser. Real implementation would need
        to adapt to specific data source format.
    """
    crime_data = {
        "quartier": quartier,
        "crime_score": 50,  # Default to median
        "categories": {},
        "national_comparison": "average",
        "trend": "stable"
    }

    # Extract crime categories (simplified patterns)
    categories = {
        "theft": ["vol", "theft", "larceny"],
        "burglary": ["cambriolage", "burglary", "break-in"],
        "assault": ["agression", "assault", "violence"],
        "vandalism": ["vandalisme", "vandalism"],
        "drug": ["drogue", "drug", "narcotic"]
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            # Look for patterns like "vol: 45" or "theft rate: 45%"
            match = re.search(
                rf"{re.escape(keyword)}[:\s]+(\d+(?:\.\d+)?)\s*%?",
                html_content,
                re.IGNORECASE
            )
            if match:
                crime_data["categories"][category] = float(match.group(1))
                break

    # Calculate overall score (if we have category data)
    if crime_data["categories"]:
        crime_data["crime_score"] = sum(crime_data["categories"].values()) / len(crime_data["categories"])

    # Extract comparison text
    if "above average" in html_content.lower() or "supérieur" in html_content.lower():
        crime_data["national_comparison"] = "above_average"
    elif "below average" in html_content.lower() or "inférieur" in html_content.lower():
        crime_data["national_comparison"] = "below_average"

    # Extract trend
    if "increasing" in html_content.lower() or "hausse" in html_content.lower():
        crime_data["trend"] = "increasing"
    elif "decreasing" in html_content.lower() or "baisse" in html_content.lower():
        crime_data["trend"] = "decreasing"

    return crime_data