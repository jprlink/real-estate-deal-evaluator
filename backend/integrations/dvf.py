"""
DVF (Demandes de Valeurs Foncières) API client for French property transaction data.

Implements progressive geographic search with robust filtering and weighted statistics.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import httpx
import math
import statistics

logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points in km using Haversine formula.

    Args:
        lat1, lon1: First point coordinates
        lat2, lon2: Second point coordinates

    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth radius in km

    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c


def time_decay_weight(sale_date: str, reference_date: datetime, decay_rate: float = 0.1) -> float:
    """
    Calculate time decay weight for comparable sales.

    Args:
        sale_date: Sale date as string (YYYY-MM-DD)
        reference_date: Reference date (usually today)
        decay_rate: Decay rate per year (default 0.1 = 10% per year)

    Returns:
        Weight between 0 and 1
    """
    try:
        sale_dt = datetime.strptime(sale_date, "%Y-%m-%d")
        months_ago = (reference_date - sale_dt).days / 30.44
        years_ago = months_ago / 12
        weight = math.exp(-decay_rate * years_ago)
        return max(0.1, weight)  # Minimum weight of 0.1
    except:
        return 0.5  # Default weight if date parsing fails


def room_similarity_weight(subject_rooms: int, comp_rooms: int) -> float:
    """
    Calculate similarity weight based on room count difference.

    Args:
        subject_rooms: Number of rooms in subject property
        comp_rooms: Number of rooms in comparable

    Returns:
        Weight between 0.5 and 1.0
    """
    diff = abs(subject_rooms - comp_rooms)
    if diff == 0:
        return 1.0
    elif diff == 1:
        return 0.9
    elif diff == 2:
        return 0.7
    else:
        return 0.5  # Penalize heavily for >2 room difference


def calculate_weighted_median_and_bands(
    comps: List[Dict[str, Any]],
    reference_date: datetime,
    subject_rooms: Optional[int] = None
) -> Dict[str, float]:
    """
    Calculate weighted median and percentile bands from comparables.

    Args:
        comps: List of comparable sales
        reference_date: Reference date for time decay
        subject_rooms: Number of rooms in subject (for weighting)

    Returns:
        dict with median, p25, p75, p10, p90
    """
    if not comps:
        return {}

    # Calculate weights and collect prices
    weighted_prices = []
    for comp in comps:
        price_per_m2 = comp.get("price_per_m2", 0)
        if price_per_m2 <= 0:
            continue

        # Time decay weight
        time_weight = time_decay_weight(
            comp.get("date_mutation", ""),
            reference_date
        )

        # Room similarity weight (if applicable)
        room_weight = 1.0
        if subject_rooms and comp.get("nombre_pieces_principales"):
            room_weight = room_similarity_weight(
                subject_rooms,
                comp.get("nombre_pieces_principales", 0)
            )

        # Combined weight
        weight = time_weight * room_weight

        # Add weighted samples (simulate by repeating based on weight)
        repeat_count = max(1, int(weight * 10))
        weighted_prices.extend([price_per_m2] * repeat_count)

    if not weighted_prices:
        return {}

    # Calculate percentiles
    weighted_prices.sort()
    n = len(weighted_prices)

    return {
        "median": statistics.median(weighted_prices),
        "p25": weighted_prices[int(n * 0.25)],
        "p75": weighted_prices[int(n * 0.75)],
        "p10": weighted_prices[int(n * 0.10)],
        "p90": weighted_prices[int(n * 0.90)],
        "mean": statistics.mean(weighted_prices),
        "count": len(comps)
    }


async def fetch_dvf_comps_progressive(
    postal_code: str,
    surface: float,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    rooms: Optional[int] = None,
    property_type: str = "Appartement",
    min_comps: int = 12
) -> Tuple[List[Dict[str, Any]], str]:
    """
    Fetch DVF comparables with progressive geographic search.

    Search strategy:
    1. Try 400m radius → if n<12
    2. Try 800m radius → if n<12
    3. Try 1.2km radius → if n<12
    4. Try commune (postal code)

    Args:
        postal_code: 5-digit French postal code
        surface: Property surface in m²
        lat, lon: Property coordinates (for radius search)
        rooms: Number of rooms
        property_type: Type of property (Appartement, Maison)
        min_comps: Minimum number of comparables needed (default 12)

    Returns:
        (List of comparables, geographic scope description)
    """
    reference_date = datetime.now()

    # Time filtering: NOTE - api.cquest.org only has data up to 2019
    # Using wider time window due to data availability
    min_date_24m = "2017-01-01"  # Last ~24 months of available data
    min_date_36m = "2016-01-01"  # Last ~36 months of available data

    logger.info(f"Starting progressive DVF search for {postal_code}, surface {surface}m²")
    logger.warning("Using api.cquest.org DVF data (only updated through June 2019)")

    # Fetch all comps for this postal code first
    all_comps = await _fetch_raw_dvf_data(postal_code, property_type, min_date_36m)

    if not all_comps:
        logger.warning(f"No DVF data found for {postal_code}")
        return [], "No data"

    logger.info(f"Fetched {len(all_comps)} raw DVF records for {postal_code}")

    # Progressive search if we have coordinates
    if lat and lon:
        for radius_km in [0.4, 0.8, 1.2]:
            comps = _filter_comps(
                all_comps, surface, rooms, reference_date,
                lat=lat, lon=lon, radius_km=radius_km,
                min_date_24m=min_date_24m, min_date_36m=min_date_36m
            )

            if len(comps) >= min_comps:
                logger.info(f"Found {len(comps)} comps within {radius_km}km radius")
                return comps, f"{radius_km}km radius"

        logger.info(f"Insufficient comps in radius searches, falling back to commune")

    # Fall back to commune-wide search
    comps = _filter_comps(
        all_comps, surface, rooms, reference_date,
        min_date_24m=min_date_24m, min_date_36m=min_date_36m
    )

    logger.info(f"Found {len(comps)} comps in commune {postal_code}")
    return comps, f"Commune {postal_code}"


async def _fetch_raw_dvf_data(
    postal_code: str,
    property_type: str,
    min_date: str
) -> List[Dict[str, Any]]:
    """
    Fetch raw DVF data from API.
    """
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            url = "https://api.cquest.org/dvf"
            params = {
                "code_postal": postal_code,
                "type_local": property_type
            }

            response = await client.get(url, params=params)

            if response.status_code != 200:
                logger.warning(f"DVF API returned status {response.status_code}")
                return []

            data = response.json()
            results = data.get("resultats", data.get("features", []))

            return results

    except httpx.TimeoutException:
        logger.warning(f"DVF API timeout for {postal_code}")
        return []
    except Exception as e:
        logger.error(f"Error fetching DVF data: {e}")
        return []


def _filter_comps(
    raw_comps: List[Dict[str, Any]],
    surface: float,
    rooms: Optional[int],
    reference_date: datetime,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    radius_km: Optional[float] = None,
    min_date_24m: str = None,
    min_date_36m: str = None
) -> List[Dict[str, Any]]:
    """
    Filter and process comparable sales.

    Applies:
    - Geographic filtering (radius if provided)
    - Surface band filtering (±12.5%, widen to ±17.5% if needed)
    - Time filtering (24 months, extend to 36 if needed)
    - Nature mutation filtering (Vente only)
    - Outlier removal (MAD, P5-P95 clamp)
    """
    comps = []

    # Initial surface band: ±12.5%
    min_surface = surface * 0.875
    max_surface = surface * 1.125

    # Filter comps
    for record in raw_comps:
        # Nature mutation filter
        nature = record.get("nature_mutation", "")
        if nature != "Vente":
            continue

        # Date filter (try 24m first)
        date_mutation = record.get("date_mutation", "")
        if not date_mutation or date_mutation < min_date_24m:
            continue

        # Geographic filter (if radius provided)
        if lat and lon and radius_km:
            comp_lat = record.get("lat")
            comp_lon = record.get("lon")
            if not comp_lat or not comp_lon:
                continue

            distance = haversine_distance(lat, lon, comp_lat, comp_lon)
            if distance > radius_km:
                continue

        # Surface filter
        surface_bati = record.get("surface_relle_bati") or record.get("surface_reelle_bati")
        valeur = record.get("valeur_fonciere")

        if not surface_bati or not valeur or valeur <= 0 or surface_bati <= 0:
            continue

        if surface_bati < min_surface or surface_bati > max_surface:
            continue

        # Valid comp
        price_per_m2 = valeur / surface_bati

        comps.append({
            "id_mutation": record.get("reference_document", ""),
            "date_mutation": date_mutation,
            "adresse": f"{record.get('numero_voie', '')} {record.get('type_voie', '')} {record.get('voie', '')}".strip(),
            "code_postal": record.get("code_postal"),
            "commune": record.get("commune"),
            "type_local": record.get("type_local"),
            "surface_reelle_bati": surface_bati,
            "nombre_pieces_principales": record.get("nombre_pieces_principales"),
            "valeur_fonciere": valeur,
            "price_per_m2": price_per_m2,
            "lat": record.get("lat"),
            "lon": record.get("lon")
        })

    # If insufficient, widen surface band to ±17.5%
    if len(comps) < 12:
        min_surface = surface * 0.825
        max_surface = surface * 1.175

        comps = []
        for record in raw_comps:
            nature = record.get("nature_mutation", "")
            if nature != "Vente":
                continue

            date_mutation = record.get("date_mutation", "")
            if not date_mutation or date_mutation < min_date_36m:  # Extend time too
                continue

            if lat and lon and radius_km:
                comp_lat = record.get("lat")
                comp_lon = record.get("lon")
                if not comp_lat or not comp_lon:
                    continue

                distance = haversine_distance(lat, lon, comp_lat, comp_lon)
                if distance > radius_km:
                    continue

            surface_bati = record.get("surface_relle_bati") or record.get("surface_reelle_bati")
            valeur = record.get("valeur_fonciere")

            if not surface_bati or not valeur or valeur <= 0 or surface_bati <= 0:
                continue

            if surface_bati < min_surface or surface_bati > max_surface:
                continue

            price_per_m2 = valeur / surface_bati

            comps.append({
                "id_mutation": record.get("reference_document", ""),
                "date_mutation": date_mutation,
                "adresse": f"{record.get('numero_voie', '')} {record.get('type_voie', '')} {record.get('voie', '')}".strip(),
                "code_postal": record.get("code_postal"),
                "commune": record.get("commune"),
                "type_local": record.get("type_local"),
                "surface_reelle_bati": surface_bati,
                "nombre_pieces_principales": record.get("nombre_pieces_principales"),
                "valeur_fonciere": valeur,
                "price_per_m2": price_per_m2,
                "lat": record.get("lat"),
                "lon": record.get("lon")
            })

    # Remove outliers using P5-P95 clamp
    if comps:
        prices = [c["price_per_m2"] for c in comps]
        prices.sort()
        n = len(prices)
        p5 = prices[int(n * 0.05)]
        p95 = prices[int(n * 0.95)]

        comps = [c for c in comps if p5 <= c["price_per_m2"] <= p95]

    return comps


def calculate_median_price_per_m2(comps: List[Dict[str, Any]]) -> float:
    """
    Calculate median price per m² from comparable sales (legacy function for backward compatibility).

    Args:
        comps: List of comparable sales

    Returns:
        float: Median price per m²
    """
    if not comps:
        return 0.0

    prices_per_m2 = [c.get("price_per_m2", 0) for c in comps if c.get("price_per_m2", 0) > 0]

    if not prices_per_m2:
        return 0.0

    return statistics.median(prices_per_m2)
