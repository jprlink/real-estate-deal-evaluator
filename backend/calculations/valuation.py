"""
Property valuation functions.

Formulas from INITIAL.md:
- Now-Cast Valuation = DVF Median (matched comps) × (1+Δ_market) × (1+Δ_listing)
  where Δ_listing aggregates transparent adjustments (price-cut %, days-on-market, condition/DPE penalties)
- Price Verdict:
  - Under-priced if < 95% of now-cast
  - Average if 95-105% of now-cast
  - Overpriced if > 105% of now-cast
- Yield on Cost = Stabilized NOI ÷ (Purchase Price + CapEx/Travaux)
"""


def nowcast_value(
    dvf_median: float,
    market_delta: float = 0.0,
    listing_delta: float = 0.0
) -> float:
    """
    Calculate now-cast property valuation using DVF comps and adjustments.

    Args:
        dvf_median: Median price from DVF comps (€/m²)
        market_delta: Market trend adjustment (e.g., 0.05 for 5% increase)
        listing_delta: Listing-specific adjustments (price cuts, DOM, condition, DPE)

    Returns:
        float: Now-cast valuation (€/m²)

    Formula:
        Now-Cast = DVF Median × (1+Δ_market) × (1+Δ_listing)
    """
    return dvf_median * (1 + market_delta) * (1 + listing_delta)


def price_verdict(property_price_per_m2: float, nowcast_value_per_m2: float) -> str:
    """
    Determine price verdict based on comparison to now-cast value.

    Args:
        property_price_per_m2: Property asking price (€/m²)
        nowcast_value_per_m2: Now-cast valuation (€/m²)

    Returns:
        str: "Under-priced", "Average", or "Overpriced"

    Logic:
        - Under-priced if < 95% of now-cast
        - Average if 95-105% of now-cast
        - Overpriced if > 105% of now-cast
    """
    if nowcast_value_per_m2 == 0:
        return "Unknown"

    ratio = property_price_per_m2 / nowcast_value_per_m2

    if ratio < 0.95:
        return "Under-priced"
    elif ratio <= 1.05:
        return "Average"
    else:
        return "Overpriced"


def listing_delta_calculation(
    price_cut_pct: float = 0.0,
    days_on_market: int = 0,
    median_dom: int = 30,
    dpe_grade: str = "D",
    condition_penalty: float = 0.0
) -> float:
    """
    Calculate listing delta from transparent adjustments.

    Args:
        price_cut_pct: Recent price cut percentage (e.g., -0.10 for -10%)
        days_on_market: Days property has been listed
        median_dom: Median days on market for area
        dpe_grade: DPE energy grade (A-G)
        condition_penalty: Condition penalty (e.g., -0.05 for poor condition)

    Returns:
        float: Aggregate listing delta adjustment

    Logic:
        - Price cuts indicate motivated seller (negative adjustment)
        - High days-on-market indicates overpricing (negative adjustment)
        - Poor DPE grade indicates higher costs (negative adjustment)
        - Poor condition indicates renovation needs (negative adjustment)
    """
    delta = 0.0

    # Price cut adjustment
    delta += price_cut_pct

    # Days on market adjustment (if significantly above median)
    if days_on_market > median_dom * 1.5:
        dom_penalty = -0.05  # 5% penalty for stale listing
        delta += dom_penalty
    elif days_on_market > median_dom * 2:
        dom_penalty = -0.10  # 10% penalty for very stale listing
        delta += dom_penalty

    # DPE grade penalty
    dpe_penalties = {
        "A": 0.05,   # Premium for excellent energy efficiency
        "B": 0.02,   # Slight premium
        "C": 0.0,    # Neutral
        "D": -0.02,  # Slight penalty
        "E": -0.05,  # Moderate penalty
        "F": -0.10,  # Significant penalty
        "G": -0.15   # Severe penalty
    }
    delta += dpe_penalties.get(dpe_grade.upper(), 0.0)

    # Condition penalty
    delta += condition_penalty

    return delta


def yield_on_cost(
    stabilized_noi: float,
    purchase_price: float,
    capex_travaux: float = 0.0
) -> float:
    """
    Calculate yield on cost (return on total investment).

    Args:
        stabilized_noi: Stabilized net operating income
        purchase_price: Property purchase price
        capex_travaux: Capital expenditures / renovation costs

    Returns:
        float: Yield on cost as a decimal (e.g., 0.06 for 6%)

    Formula:
        Yield on Cost = Stabilized NOI ÷ (Purchase Price + CapEx/Travaux)
    """
    total_investment = purchase_price + capex_travaux
    if total_investment == 0:
        return 0.0
    return stabilized_noi / total_investment