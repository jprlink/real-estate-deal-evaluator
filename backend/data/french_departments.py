"""
Complete French department and postal code mapping.

Maps department codes (first 2 digits of postal code) to their main cities.
For precise city detection, use specific postal code mappings where available.
"""

from typing import Dict, Optional, Tuple

# Department code to (department_name, main_city) mapping
# Covers all 101 French departments including overseas territories
FRENCH_DEPARTMENTS: Dict[str, Tuple[str, str]] = {
    # Auvergne-Rhône-Alpes
    "01": ("Ain", "Bourg-en-Bresse"),
    "03": ("Allier", "Moulins"),
    "07": ("Ardèche", "Privas"),
    "15": ("Cantal", "Aurillac"),
    "26": ("Drôme", "Valence"),
    "38": ("Isère", "Grenoble"),
    "42": ("Loire", "Saint-Étienne"),
    "43": ("Haute-Loire", "Le Puy-en-Velay"),
    "63": ("Puy-de-Dôme", "Clermont-Ferrand"),
    "69": ("Rhône", "Lyon"),
    "73": ("Savoie", "Chambéry"),
    "74": ("Haute-Savoie", "Annecy"),

    # Bourgogne-Franche-Comté
    "21": ("Côte-d'Or", "Dijon"),
    "25": ("Doubs", "Besançon"),
    "39": ("Jura", "Lons-le-Saunier"),
    "58": ("Nièvre", "Nevers"),
    "70": ("Haute-Saône", "Vesoul"),
    "71": ("Saône-et-Loire", "Mâcon"),
    "89": ("Yonne", "Auxerre"),
    "90": ("Territoire de Belfort", "Belfort"),

    # Bretagne
    "22": ("Côtes-d'Armor", "Saint-Brieuc"),
    "29": ("Finistère", "Brest"),
    "35": ("Ille-et-Vilaine", "Rennes"),
    "56": ("Morbihan", "Vannes"),

    # Centre-Val de Loire
    "18": ("Cher", "Bourges"),
    "28": ("Eure-et-Loir", "Chartres"),
    "36": ("Indre", "Châteauroux"),
    "37": ("Indre-et-Loire", "Tours"),
    "41": ("Loir-et-Cher", "Blois"),
    "45": ("Loiret", "Orléans"),

    # Corse
    "2A": ("Corse-du-Sud", "Ajaccio"),
    "2B": ("Haute-Corse", "Bastia"),
    "20": ("Corse", "Ajaccio"),  # Fallback for Corsica

    # Grand Est
    "08": ("Ardennes", "Charleville-Mézières"),
    "10": ("Aube", "Troyes"),
    "51": ("Marne", "Reims"),
    "52": ("Haute-Marne", "Chaumont"),
    "54": ("Meurthe-et-Moselle", "Nancy"),
    "55": ("Meuse", "Bar-le-Duc"),
    "57": ("Moselle", "Metz"),
    "67": ("Bas-Rhin", "Strasbourg"),
    "68": ("Haut-Rhin", "Mulhouse"),
    "88": ("Vosges", "Épinal"),

    # Hauts-de-France
    "02": ("Aisne", "Laon"),
    "59": ("Nord", "Lille"),
    "60": ("Oise", "Beauvais"),
    "62": ("Pas-de-Calais", "Calais"),
    "80": ("Somme", "Amiens"),

    # Île-de-France
    "75": ("Paris", "Paris"),
    "77": ("Seine-et-Marne", "Melun"),
    "78": ("Yvelines", "Versailles"),
    "91": ("Essonne", "Évry-Courcouronnes"),
    "92": ("Hauts-de-Seine", "Nanterre"),
    "93": ("Seine-Saint-Denis", "Bobigny"),
    "94": ("Val-de-Marne", "Créteil"),
    "95": ("Val-d'Oise", "Cergy"),

    # Normandie
    "14": ("Calvados", "Caen"),
    "27": ("Eure", "Évreux"),
    "50": ("Manche", "Saint-Lô"),
    "61": ("Orne", "Alençon"),
    "76": ("Seine-Maritime", "Rouen"),

    # Nouvelle-Aquitaine
    "16": ("Charente", "Angoulême"),
    "17": ("Charente-Maritime", "La Rochelle"),
    "19": ("Corrèze", "Tulle"),
    "23": ("Creuse", "Guéret"),
    "24": ("Dordogne", "Périgueux"),
    "33": ("Gironde", "Bordeaux"),
    "40": ("Landes", "Mont-de-Marsan"),
    "47": ("Lot-et-Garonne", "Agen"),
    "64": ("Pyrénées-Atlantiques", "Pau"),
    "79": ("Deux-Sèvres", "Niort"),
    "86": ("Vienne", "Poitiers"),
    "87": ("Haute-Vienne", "Limoges"),

    # Occitanie
    "09": ("Ariège", "Foix"),
    "11": ("Aude", "Carcassonne"),
    "12": ("Aveyron", "Rodez"),
    "30": ("Gard", "Nîmes"),
    "31": ("Haute-Garonne", "Toulouse"),
    "32": ("Gers", "Auch"),
    "34": ("Hérault", "Montpellier"),
    "46": ("Lot", "Cahors"),
    "48": ("Lozère", "Mende"),
    "65": ("Hautes-Pyrénées", "Tarbes"),
    "66": ("Pyrénées-Orientales", "Perpignan"),
    "81": ("Tarn", "Albi"),
    "82": ("Tarn-et-Garonne", "Montauban"),

    # Pays de la Loire
    "44": ("Loire-Atlantique", "Nantes"),
    "49": ("Maine-et-Loire", "Angers"),
    "53": ("Mayenne", "Laval"),
    "72": ("Sarthe", "Le Mans"),
    "85": ("Vendée", "La Roche-sur-Yon"),

    # Provence-Alpes-Côte d'Azur
    "04": ("Alpes-de-Haute-Provence", "Digne-les-Bains"),
    "05": ("Hautes-Alpes", "Gap"),
    "06": ("Alpes-Maritimes", "Nice"),
    "13": ("Bouches-du-Rhône", "Marseille"),
    "83": ("Var", "Toulon"),
    "84": ("Vaucluse", "Avignon"),

    # Overseas departments
    "971": ("Guadeloupe", "Basse-Terre"),
    "972": ("Martinique", "Fort-de-France"),
    "973": ("Guyane", "Cayenne"),
    "974": ("La Réunion", "Saint-Denis"),
    "976": ("Mayotte", "Mamoudzou"),
}

# Specific postal code mappings for major cities
# This overrides department-level detection for precision
SPECIFIC_POSTAL_CODES: Dict[str, str] = {
    # Haute-Savoie (74) - Major cities
    "74000": "Annecy",
    "74100": "Annemasse",
    "74200": "Thonon-les-Bains",
    "74300": "Cluses",
    "74400": "Chamonix-Mont-Blanc",
    "74500": "Évian-les-Bains",
    "74600": "Seynod",
    "74700": "Sallanches",
    "74800": "La Roche-sur-Foron",
    "74940": "Annecy-le-Vieux",

    # Add more specific cities as needed for precision
    # (The system will fall back to department main city if not found)
}


def get_city_from_department(postal_code: str) -> Optional[str]:
    """
    Get main city for a department based on postal code.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        str: Main city of the department, or None if department not found
    """
    if not postal_code or len(postal_code) < 2:
        return None

    # Handle overseas departments (3-digit codes)
    if postal_code.startswith("97") and len(postal_code) == 5:
        dept_code = postal_code[:3]
        if dept_code in FRENCH_DEPARTMENTS:
            return FRENCH_DEPARTMENTS[dept_code][1]

    # Handle Corsica special case (2A, 2B)
    if postal_code.startswith("20"):
        second_digit = postal_code[2] if len(postal_code) > 2 else "0"
        if second_digit in "01234":
            return "Ajaccio"  # Corse-du-Sud (2A)
        else:
            return "Bastia"  # Haute-Corse (2B)

    # Standard 2-digit department code
    dept_code = postal_code[:2]
    if dept_code in FRENCH_DEPARTMENTS:
        return FRENCH_DEPARTMENTS[dept_code][1]

    return None


def get_department_name(postal_code: str) -> Optional[str]:
    """
    Get department name from postal code.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        str: Department name, or None if not found
    """
    if not postal_code or len(postal_code) < 2:
        return None

    # Handle overseas departments
    if postal_code.startswith("97") and len(postal_code) == 5:
        dept_code = postal_code[:3]
        if dept_code in FRENCH_DEPARTMENTS:
            return FRENCH_DEPARTMENTS[dept_code][0]

    # Handle Corsica
    if postal_code.startswith("20"):
        second_digit = postal_code[2] if len(postal_code) > 2 else "0"
        if second_digit in "01234":
            return "Corse-du-Sud"
        else:
            return "Haute-Corse"

    # Standard departments
    dept_code = postal_code[:2]
    if dept_code in FRENCH_DEPARTMENTS:
        return FRENCH_DEPARTMENTS[dept_code][0]

    return None
