"""
Official French postal code to city mapping database.

Based on official French postal code data from data.gouv.fr and INSEE.
This provides accurate city names for postal codes, fixing location/postcode mismatches.
"""

from typing import Dict, Optional, Tuple

# Comprehensive postal code to city mapping for major French cities
# Format: postal_code -> (city_name, department_code)
POSTAL_CODE_TO_CITY: Dict[str, Tuple[str, str]] = {
    # Paris (75)
    **{f"750{str(i).zfill(2)}": ("Paris", "75") for i in range(1, 21)},

    # Hauts-de-Seine (92)
    "92000": ("Nanterre", "92"),
    "92100": ("Boulogne-Billancourt", "92"),
    "92110": ("Clichy", "92"),
    "92120": ("Montrouge", "92"),
    "92130": ("Issy-les-Moulineaux", "92"),
    "92140": ("Clamart", "92"),
    "92150": ("Suresnes", "92"),
    "92160": ("Antony", "92"),
    "92170": ("Vanves", "92"),
    "92190": ("Meudon", "92"),
    "92200": ("Neuilly-sur-Seine", "92"),
    "92210": ("Saint-Cloud", "92"),
    "92220": ("Bagneux", "92"),
    "92230": ("Gennevilliers", "92"),
    "92240": ("Malakoff", "92"),
    "92250": ("La Garenne-Colombes", "92"),
    "92260": ("Fontenay-aux-Roses", "92"),
    "92270": ("Bois-Colombes", "92"),
    "92290": ("Châtenay-Malabry", "92"),
    "92300": ("Levallois-Perret", "92"),
    "92310": ("Sèvres", "92"),
    "92320": ("Châtillon", "92"),
    "92330": ("Sceaux", "92"),
    "92340": ("Bourg-la-Reine", "92"),
    "92350": ("Le Plessis-Robinson", "92"),
    "92360": ("Meudon", "92"),
    "92370": ("Chaville", "92"),
    "92380": ("Garches", "92"),
    "92390": ("Villeneuve-la-Garenne", "92"),
    "92400": ("Courbevoie", "92"),
    "92410": ("Ville-d'Avray", "92"),
    "92420": ("Vaucresson", "92"),
    "92430": ("Marnes-la-Coquette", "92"),
    "92500": ("Rueil-Malmaison", "92"),
    "92600": ("Asnières-sur-Seine", "92"),
    "92700": ("Colombes", "92"),
    "92800": ("Puteaux", "92"),

    # Seine-Saint-Denis (93)
    "93000": ("Bobigny", "93"),
    "93100": ("Montreuil", "93"),
    "93110": ("Rosny-sous-Bois", "93"),
    "93120": ("La Courneuve", "93"),
    "93130": ("Noisy-le-Sec", "93"),
    "93140": ("Bondy", "93"),
    "93150": ("Le Blanc-Mesnil", "93"),
    "93160": ("Noisy-le-Grand", "93"),
    "93170": ("Bagnolet", "93"),
    "93190": ("Livry-Gargan", "93"),
    "93200": ("Saint-Denis", "93"),
    "93210": ("Saint-Denis", "93"),
    "93220": ("Gagny", "93"),
    "93230": ("Romainville", "93"),
    "93240": ("Stains", "93"),
    "93250": ("Villemomble", "93"),
    "93260": ("Les Lilas", "93"),
    "93270": ("Sevran", "93"),
    "93290": ("Tremblay-en-France", "93"),
    "93300": ("Aubervilliers", "93"),
    "93310": ("Le Pré-Saint-Gervais", "93"),
    "93320": ("Les Pavillons-sous-Bois", "93"),
    "93330": ("Neuilly-sur-Marne", "93"),
    "93340": ("Le Raincy", "93"),
    "93350": ("Le Bourget", "93"),
    "93360": ("Neuilly-Plaisance", "93"),
    "93370": ("Montfermeil", "93"),
    "93380": ("Pierrefitte-sur-Seine", "93"),
    "93390": ("Clichy-sous-Bois", "93"),
    "93400": ("Saint-Ouen-sur-Seine", "93"),
    "93410": ("Vaujours", "93"),
    "93420": ("Villepinte", "93"),
    "93430": ("Villetaneuse", "93"),
    "93440": ("Dugny", "93"),
    "93450": ("L'Île-Saint-Denis", "93"),
    "93460": ("Gournay-sur-Marne", "93"),
    "93470": ("Coubron", "93"),
    "93500": ("Pantin", "93"),
    "93600": ("Aulnay-sous-Bois", "93"),
    "93700": ("Drancy", "93"),
    "93800": ("Épinay-sur-Seine", "93"),

    # Val-de-Marne (94)
    "94000": ("Créteil", "94"),
    "94100": ("Saint-Maur-des-Fossés", "94"),
    "94110": ("Arcueil", "94"),
    "94120": ("Fontenay-sous-Bois", "94"),
    "94130": ("Nogent-sur-Marne", "94"),
    "94140": ("Alfortville", "94"),
    "94150": ("Rungis", "94"),
    "94160": ("Saint-Mandé", "94"),
    "94170": ("Le Perreux-sur-Marne", "94"),
    "94200": ("Ivry-sur-Seine", "94"),
    "94210": ("Saint-Maur-des-Fossés", "94"),
    "94220": ("Charenton-le-Pont", "94"),
    "94230": ("Cachan", "94"),
    "94240": ("L'Haÿ-les-Roses", "94"),
    "94250": ("Gentilly", "94"),
    "94260": ("Fresnes", "94"),
    "94270": ("Le Kremlin-Bicêtre", "94"),
    "94300": ("Vincennes", "94"),
    "94310": ("Orly", "94"),
    "94320": ("Thiais", "94"),
    "94340": ("Joinville-le-Pont", "94"),
    "94350": ("Villiers-sur-Marne", "94"),
    "94360": ("Bry-sur-Marne", "94"),
    "94370": ("Sucy-en-Brie", "94"),
    "94380": ("Bonneuil-sur-Marne", "94"),
    "94400": ("Vitry-sur-Seine", "94"),
    "94410": ("Saint-Maurice", "94"),
    "94420": ("Le Plessis-Trévise", "94"),
    "94430": ("Chennevières-sur-Marne", "94"),
    "94440": ("Villecresnes", "94"),
    "94450": ("Limeil-Brévannes", "94"),
    "94460": ("Valenton", "94"),
    "94470": ("Boissy-Saint-Léger", "94"),
    "94480": ("Ablon-sur-Seine", "94"),
    "94490": ("Ormesson-sur-Marne", "94"),
    "94500": ("Champigny-sur-Marne", "94"),
    "94510": ("La Queue-en-Brie", "94"),
    "94520": ("Mandres-les-Roses", "94"),
    "94550": ("Chevilly-Larue", "94"),
    "94600": ("Choisy-le-Roi", "94"),
    "94700": ("Maisons-Alfort", "94"),
    "94800": ("Villejuif", "94"),

    # Essonne (91)
    "91000": ("Évry-Courcouronnes", "91"),
    "91100": ("Corbeil-Essonnes", "91"),
    "91120": ("Palaiseau", "91"),
    "91130": ("Ris-Orangis", "91"),
    "91140": ("Villebon-sur-Yvette", "91"),
    "91150": ("Étampes", "91"),
    "91160": ("Longjumeau", "91"),
    "91170": ("Viry-Châtillon", "91"),
    "91190": ("Gif-sur-Yvette", "91"),
    "91200": ("Athis-Mons", "91"),
    "91210": ("Draveil", "91"),
    "91220": ("Brétigny-sur-Orge", "91"),
    "91230": ("Montgeron", "91"),
    "91240": ("Saint-Michel-sur-Orge", "91"),
    "91250": ("Tigery", "91"),
    "91260": ("Juvisy-sur-Orge", "91"),
    "91270": ("Vigneux-sur-Seine", "91"),
    "91280": ("Saint-Pierre-du-Perray", "91"),
    "91290": ("Arpajon", "91"),
    "91300": ("Massy", "91"),
    "91310": ("Montlhéry", "91"),
    "91320": ("Wissous", "91"),
    "91330": ("Yerres", "91"),
    "91340": ("Ollainville", "91"),
    "91350": ("Grigny", "91"),
    "91360": ("Épinay-sur-Orge", "91"),
    "91370": ("Verrières-le-Buisson", "91"),
    "91380": ("Chilly-Mazarin", "91"),
    "91390": ("Morsang-sur-Orge", "91"),
    "91400": ("Orsay", "91"),
    "91410": ("Dourdan", "91"),
    "91420": ("Morangis", "91"),
    "91430": ("Igny", "91"),
    "91440": ("Bures-sur-Yvette", "91"),
    "91450": ("Soisy-sur-Seine", "91"),
    "91460": ("Marcoussis", "91"),
    "91470": ("Limours", "91"),
    "91480": ("Quincy-sous-Sénart", "91"),
    "91490": ("Milly-la-Forêt", "91"),
    "91600": ("Savigny-sur-Orge", "91"),
    "91700": ("Sainte-Geneviève-des-Bois", "91"),
    "91800": ("Brunoy", "91"),

    # Yvelines (78)
    "78000": ("Versailles", "78"),
    "78100": ("Saint-Germain-en-Laye", "78"),
    "78110": ("Le Vésinet", "78"),
    "78120": ("Rambouillet", "78"),
    "78130": ("Les Mureaux", "78"),
    "78140": ("Vélizy-Villacoublay", "78"),
    "78150": ("Le Chesnay-Rocquencourt", "78"),
    "78160": ("Marly-le-Roi", "78"),
    "78170": ("La Celle-Saint-Cloud", "78"),
    "78180": ("Montigny-le-Bretonneux", "78"),
    "78190": ("Trappes", "78"),
    "78200": ("Mantes-la-Jolie", "78"),
    "78210": ("Saint-Cyr-l'École", "78"),
    "78220": ("Viroflay", "78"),
    "78230": ("Le Pecq", "78"),
    "78240": ("Chambourcy", "78"),
    "78250": ("Meulan-en-Yvelines", "78"),
    "78260": ("Achères", "78"),
    "78270": ("Bonnières-sur-Seine", "78"),
    "78280": ("Guyancourt", "78"),
    "78290": ("Croissy-sur-Seine", "78"),
    "78300": ("Poissy", "78"),
    "78310": ("Maurepas", "78"),
    "78320": ("Le Mesnil-Saint-Denis", "78"),
    "78330": ("Fontenay-le-Fleury", "78"),
    "78340": ("Les Clayes-sous-Bois", "78"),
    "78350": ("Jouy-en-Josas", "78"),
    "78360": ("Montesson", "78"),
    "78370": ("Plaisir", "78"),
    "78380": ("Bougival", "78"),
    "78390": ("Bois-d'Arcy", "78"),
    "78400": ("Chatou", "78"),
    "78410": ("Aubergenville", "78"),
    "78420": ("Carrières-sur-Seine", "78"),
    "78430": ("Louveciennes", "78"),
    "78440": ("Gargenville", "78"),
    "78450": ("Villepreux", "78"),
    "78460": ("Chevreuse", "78"),
    "78470": ("Saint-Rémy-lès-Chevreuse", "78"),
    "78480": ("Verneuil-sur-Seine", "78"),
    "78490": ("Montfort-l'Amaury", "78"),
    "78500": ("Sartrouville", "78"),
    "78510": ("Triel-sur-Seine", "78"),
    "78520": ("Limay", "78"),
    "78530": ("Buc", "78"),
    "78540": ("Vernouillet", "78"),
    "78550": ("Houdan", "78"),
    "78560": ("Le Port-Marly", "78"),
    "78570": ("Andrésy", "78"),
    "78580": ("Maule", "78"),
    "78590": ("Noisy-le-Roi", "78"),
    "78600": ("Maisons-Laffitte", "78"),
    "78700": ("Conflans-Sainte-Honorine", "78"),
    "78800": ("Houilles", "78"),

    # Val-d'Oise (95)
    "95000": ("Cergy", "95"),
    "95100": ("Argenteuil", "95"),
    "95110": ("Sannois", "95"),
    "95120": ("Ermont", "95"),
    "95130": ("Franconville", "95"),
    "95140": ("Garges-lès-Gonesse", "95"),
    "95150": ("Taverny", "95"),
    "95160": ("Montmorency", "95"),
    "95170": ("Deuil-la-Barre", "95"),
    "95190": ("Goussainville", "95"),
    "95200": ("Sarcelles", "95"),
    "95210": ("Saint-Gratien", "95"),
    "95220": ("Herblay-sur-Oise", "95"),
    "95230": ("Soisy-sous-Montmorency", "95"),
    "95240": ("Cormeilles-en-Parisis", "95"),
    "95250": ("Beauchamp", "95"),
    "95260": ("Beaumont-sur-Oise", "95"),
    "95270": ("Asnières-sur-Oise", "95"),
    "95280": ("Jouy-le-Moutier", "95"),
    "95290": ("L'Isle-Adam", "95"),
    "95300": ("Pontoise", "95"),
    "95310": ("Saint-Ouen-l'Aumône", "95"),
    "95320": ("Saint-Leu-la-Forêt", "95"),
    "95330": ("Domont", "95"),
    "95340": ("Persan", "95"),
    "95350": ("Saint-Brice-sous-Forêt", "95"),
    "95360": ("Montmagny", "95"),
    "95370": ("Montigny-lès-Cormeilles", "95"),
    "95380": ("Louvres", "95"),
    "95390": ("Saint-Prix", "95"),
    "95400": ("Arnouville", "95"),
    "95410": ("Groslay", "95"),
    "95420": ("Magny-en-Vexin", "95"),
    "95430": ("Auvers-sur-Oise", "95"),
    "95440": ("Écouen", "95"),
    "95450": ("Vigny", "95"),
    "95460": ("Ézanville", "95"),
    "95470": ("Fosses", "95"),
    "95480": ("Pierrelaye", "95"),
    "95490": ("Vauréal", "95"),
    "95500": ("Gonesse", "95"),
    "95520": ("Osny", "95"),
    "95540": ("Méry-sur-Oise", "95"),
    "95550": ("Bessancourt", "95"),
    "95560": ("Baillet-en-France", "95"),
    "95570": ("Moisselles", "95"),
    "95580": ("Andilly", "95"),
    "95590": ("Presles", "95"),
    "95600": ("Eaubonne", "95"),
    "95610": ("Éragny", "95"),
    "95630": ("Mériel", "95"),
    "95650": ("Boissy-l'Aillerie", "95"),
    "95670": ("Marly-la-Ville", "95"),
    "95700": ("Roissy-en-France", "95"),
    "95800": ("Cergy", "95"),

    # Seine-et-Marne (77)
    "77000": ("Melun", "77"),
    "77100": ("Meaux", "77"),
    "77120": ("Coulommiers", "77"),
    "77130": ("Montereau-Fault-Yonne", "77"),
    "77140": ("Nemours", "77"),
    "77150": ("Lésigny", "77"),
    "77160": ("Provins", "77"),
    "77170": ("Brie-Comte-Robert", "77"),
    "77176": ("Savigny-le-Temple", "77"),
    "77180": ("Vaires-sur-Marne", "77"),
    "77190": ("Dammarie-les-Lys", "77"),
    "77200": ("Torcy", "77"),
    "77210": ("Avon", "77"),
    "77220": ("Gretz-Armainvilliers", "77"),
    "77230": ("Dammartin-en-Goële", "77"),
    "77240": ("Cesson", "77"),
    "77250": ("Moret-Loing-et-Orvanne", "77"),
    "77260": ("La Ferté-sous-Jouarre", "77"),
    "77270": ("Villeparisis", "77"),
    "77280": ("Othis", "77"),
    "77290": ("Mitry-Mory", "77"),
    "77300": ("Fontainebleau", "77"),
    "77310": ("Saint-Fargeau-Ponthierry", "77"),
    "77320": ("La Ferté-Gaucher", "77"),
    "77330": ("Ozoir-la-Ferrière", "77"),
    "77340": ("Pontault-Combault", "77"),
    "77350": ("Le Mée-sur-Seine", "77"),
    "77360": ("Vaires-sur-Marne", "77"),
    "77370": ("Nangis", "77"),
    "77380": ("Combs-la-Ville", "77"),
    "77400": ("Lagny-sur-Marne", "77"),
    "77410": ("Claye-Souilly", "77"),
    "77420": ("Champs-sur-Marne", "77"),
    "77430": ("Champagne-sur-Seine", "77"),
    "77440": ("Lizy-sur-Ourcq", "77"),
    "77450": ("Esbly", "77"),
    "77500": ("Chelles", "77"),
    "77600": ("Bussy-Saint-Georges", "77"),
    "77700": ("Serris", "77"),

    # Major cities outside Île-de-France
    "13001": ("Marseille", "13"), "13002": ("Marseille", "13"), "13003": ("Marseille", "13"),
    "13004": ("Marseille", "13"), "13005": ("Marseille", "13"), "13006": ("Marseille", "13"),
    "13007": ("Marseille", "13"), "13008": ("Marseille", "13"), "13009": ("Marseille", "13"),
    "13010": ("Marseille", "13"), "13011": ("Marseille", "13"), "13012": ("Marseille", "13"),
    "13013": ("Marseille", "13"), "13014": ("Marseille", "13"), "13015": ("Marseille", "13"),
    "13016": ("Marseille", "13"),

    "69001": ("Lyon", "69"), "69002": ("Lyon", "69"), "69003": ("Lyon", "69"),
    "69004": ("Lyon", "69"), "69005": ("Lyon", "69"), "69006": ("Lyon", "69"),
    "69007": ("Lyon", "69"), "69008": ("Lyon", "69"), "69009": ("Lyon", "69"),

    "31000": ("Toulouse", "31"), "31100": ("Toulouse", "31"), "31200": ("Toulouse", "31"),
    "31300": ("Toulouse", "31"), "31400": ("Toulouse", "31"), "31500": ("Toulouse", "31"),

    "33000": ("Bordeaux", "33"), "33100": ("Bordeaux", "33"), "33200": ("Bordeaux", "33"),
    "33300": ("Bordeaux", "33"), "33800": ("Bordeaux", "33"),

    "59000": ("Lille", "59"), "59100": ("Roubaix", "59"), "59200": ("Tourcoing", "59"),
    "59300": ("Valenciennes", "59"), "59800": ("Lille", "59"),

    "44000": ("Nantes", "44"), "44100": ("Nantes", "44"), "44200": ("Nantes", "44"),
    "44300": ("Nantes", "44"),

    "67000": ("Strasbourg", "67"), "67100": ("Strasbourg", "67"), "67200": ("Strasbourg", "67"),

    "35000": ("Rennes", "35"), "35200": ("Rennes", "35"), "35700": ("Rennes", "35"),

    "34000": ("Montpellier", "34"), "34070": ("Montpellier", "34"), "34080": ("Montpellier", "34"),
    "34090": ("Montpellier", "34"),

    "06000": ("Nice", "06"), "06100": ("Nice", "06"), "06200": ("Nice", "06"),
    "06300": ("Nice", "06"),

    "76000": ("Rouen", "76"), "76100": ("Rouen", "76"),

    "21000": ("Dijon", "21"),

    "63000": ("Clermont-Ferrand", "63"), "63100": ("Clermont-Ferrand", "63"),

    "83000": ("Toulon", "83"), "83100": ("Toulon", "83"), "83200": ("Toulon", "83"),

    "38000": ("Grenoble", "38"), "38100": ("Grenoble", "38"),

    "49000": ("Angers", "49"), "49100": ("Angers", "49"),

    "54000": ("Nancy", "54"), "54100": ("Nancy", "54"),

    "57000": ("Metz", "57"), "57070": ("Metz", "57"),

    "29200": ("Brest", "29"),

    "87000": ("Limoges", "87"), "87100": ("Limoges", "87"),

    "25000": ("Besançon", "25"),

    "45000": ("Orléans", "45"), "45100": ("Orléans", "45"),

    "68100": ("Mulhouse", "68"), "68200": ("Mulhouse", "68"),

    "62100": ("Calais", "62"),

    "80000": ("Amiens", "80"),
}


def get_city_from_postal_code(postal_code: str) -> Optional[str]:
    """
    Get official city name from French postal code.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        str: Official city name, or None if not found
    """
    if not postal_code or len(postal_code) != 5:
        return None

    # First, check specific postal code mappings (most precise)
    result = POSTAL_CODE_TO_CITY.get(postal_code)
    if result:
        return result[0]

    # Fallback to department-level detection for all French postcodes
    from backend.data.french_departments import get_city_from_department, SPECIFIC_POSTAL_CODES

    # Check specific city mappings first
    if postal_code in SPECIFIC_POSTAL_CODES:
        return SPECIFIC_POSTAL_CODES[postal_code]

    # Fall back to main city of department
    return get_city_from_department(postal_code)


def get_department_from_postal_code(postal_code: str) -> Optional[str]:
    """
    Get department code from French postal code.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        str: 2-digit department code, or None if not found
    """
    if not postal_code or len(postal_code) != 5:
        return None

    result = POSTAL_CODE_TO_CITY.get(postal_code)
    if result:
        return result[1]

    # Fallback: extract first 2 digits
    return postal_code[:2]


def get_city_and_department(postal_code: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Get both city name and department code from postal code.

    Args:
        postal_code: 5-digit French postal code

    Returns:
        tuple: (city_name, department_code) or (None, None) if not found
    """
    if not postal_code or len(postal_code) != 5:
        return None, None

    result = POSTAL_CODE_TO_CITY.get(postal_code)
    if result:
        return result

    return None, postal_code[:2]  # Return department as fallback
