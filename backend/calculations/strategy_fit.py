"""
Strategy fit scoring for different real estate investment profiles.

From INITIAL.md:
Strategy Fit (0–100) with reasons, sorted best-fit first:
- Owner-occupier
- Location nue (unfurnished)
- LMNP (furnished, micro-BIC)
- Colocation
- Value-Add / déficit foncier

Each card shows Pros & Cons tied to actual metrics (TMC vs rent, DSCR, IRR, compliance, bedrooms, discount vs median).

Formula:
Fit = Σ(w_i · s_i^norm)
with profile-specific weights and normalized metric scores.
"""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class StrategyFit:
    """Strategy fit score with reasons."""
    strategy: str
    score: float  # 0-100
    reasons: List[str]
    pros: List[str]
    cons: List[str]


def normalize_score(value: float, min_val: float, max_val: float) -> float:
    """
    Normalize a value to 0-100 scale.

    Args:
        value: Value to normalize
        min_val: Minimum value (maps to 0)
        max_val: Maximum value (maps to 100)

    Returns:
        float: Normalized score (0-100)
    """
    if max_val == min_val:
        return 50.0
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0.0, min(100.0, normalized))


def calculate_owner_occupier_fit(
    tmc: float,
    market_rent: float,
    dscr: float,
    price_discount_pct: float,
    legal_rent_compliant: bool
) -> StrategyFit:
    """
    Calculate fit score for owner-occupier strategy.

    Args:
        tmc: Total monthly cost
        market_rent: Market rent for similar properties
        dscr: Debt service coverage ratio
        price_discount_pct: Discount vs median (e.g., -0.10 for 10% below)
        legal_rent_compliant: Whether property complies with rent control

    Returns:
        StrategyFit: Strategy fit with score and reasons
    """
    pros = []
    cons = []
    reasons = []

    # Calculate net housing cost vs renting
    net_cost_vs_rent = tmc - market_rent

    # Score components (0-100 each)
    cost_score = normalize_score(-net_cost_vs_rent, -1000, 1000)  # Better if TMC < rent
    discount_score = normalize_score(-price_discount_pct, -0.20, 0.05)  # Better with discount

    # Weighted average
    score = (cost_score * 0.6 + discount_score * 0.4)

    # Pros/Cons
    if net_cost_vs_rent < 0:
        pros.append(f"Monthly cost €{abs(net_cost_vs_rent):.0f} less than renting")
        reasons.append("Ownership cheaper than renting")
    else:
        cons.append(f"Monthly cost €{net_cost_vs_rent:.0f} more than renting")

    if price_discount_pct < -0.05:
        pros.append(f"Property priced {abs(price_discount_pct)*100:.0f}% below market")
    elif price_discount_pct > 0.05:
        cons.append(f"Property priced {price_discount_pct*100:.0f}% above market")

    pros.append("Build equity through principal payments")
    pros.append("Stable housing costs (fixed-rate mortgage)")

    cons.append("Lower liquidity vs renting")
    cons.append("Maintenance and repair responsibilities")

    return StrategyFit(
        strategy="Owner-occupier",
        score=score,
        reasons=reasons,
        pros=pros,
        cons=cons
    )


def calculate_location_nue_fit(
    dscr: float,
    irr: float,
    legal_rent_compliant: bool,
    bedrooms: int
) -> StrategyFit:
    """
    Calculate fit score for location nue (unfurnished rental) strategy.

    Args:
        dscr: Debt service coverage ratio
        irr: Internal rate of return
        legal_rent_compliant: Whether rent complies with encadrement
        bedrooms: Number of bedrooms

    Returns:
        StrategyFit: Strategy fit with score and reasons
    """
    pros = []
    cons = []
    reasons = []

    # Score components
    dscr_score = normalize_score(dscr, 0.8, 1.5)  # DSCR > 1.2 is good
    irr_score = normalize_score(irr, 0.02, 0.12)  # IRR 2-12% range

    # Weighted average
    score = (dscr_score * 0.5 + irr_score * 0.5)

    # Adjust for compliance
    if not legal_rent_compliant:
        score *= 0.7  # 30% penalty for non-compliance
        cons.append("Rent exceeds legal ceiling (encadrement)")
        reasons.append("Legal risk with current rent")

    # Pros/Cons
    if dscr > 1.2:
        pros.append(f"Strong cash flow (DSCR: {dscr:.2f})")
        reasons.append("Positive monthly cash flow")
    elif dscr < 1.0:
        cons.append(f"Negative cash flow (DSCR: {dscr:.2f})")
        reasons.append("Monthly losses expected")

    if irr > 0.08:
        pros.append(f"Excellent IRR: {irr*100:.1f}%")
    elif irr < 0.04:
        cons.append(f"Low IRR: {irr*100:.1f}%")

    pros.append("30% flat tax abatement (micro-foncier)")
    pros.append("Long-term tenant stability")

    cons.append("Lower rent vs furnished (typically 20-30% less)")
    cons.append("Tenant protections favor long leases")

    return StrategyFit(
        strategy="Location nue (unfurnished)",
        score=score,
        reasons=reasons,
        pros=pros,
        cons=cons
    )


def calculate_lmnp_fit(
    dscr: float,
    irr: float,
    legal_rent_compliant: bool,
    bedrooms: int
) -> StrategyFit:
    """
    Calculate fit score for LMNP (furnished rental) strategy.

    Args:
        dscr: Debt service coverage ratio
        irr: Internal rate of return
        legal_rent_compliant: Whether rent complies with encadrement
        bedrooms: Number of bedrooms

    Returns:
        StrategyFit: Strategy fit with score and reasons
    """
    pros = []
    cons = []
    reasons = []

    # Score components
    dscr_score = normalize_score(dscr, 0.8, 1.5)
    irr_score = normalize_score(irr, 0.03, 0.15)  # Higher IRR potential for furnished

    # Weighted average
    score = (dscr_score * 0.5 + irr_score * 0.5)

    # Adjust for compliance
    if not legal_rent_compliant:
        score *= 0.7
        cons.append("Furnished rent exceeds legal ceiling")

    # Pros/Cons
    if dscr > 1.2:
        pros.append(f"Strong cash flow (DSCR: {dscr:.2f})")
        reasons.append("Positive monthly cash flow")
    elif dscr < 1.0:
        cons.append(f"Negative cash flow (DSCR: {dscr:.2f})")

    if irr > 0.10:
        pros.append(f"Excellent IRR: {irr*100:.1f}%")
        reasons.append("High return potential")
    elif irr < 0.05:
        cons.append(f"Low IRR: {irr*100:.1f}%")

    pros.append("50% gross rent abatement (micro-BIC)")
    pros.append("Higher rent vs unfurnished (20-30% premium)")
    pros.append("Flexible tenant turnover")

    cons.append("Furniture and equipment costs")
    cons.append("Higher vacancy risk with short leases")
    cons.append("More intensive management required")

    return StrategyFit(
        strategy="LMNP (furnished, micro-BIC)",
        score=score,
        reasons=reasons,
        pros=pros,
        cons=cons
    )


def calculate_colocation_fit(
    dscr: float,
    irr: float,
    bedrooms: int,
    legal_rent_compliant: bool
) -> StrategyFit:
    """
    Calculate fit score for colocation (flatshare) strategy.

    Args:
        dscr: Debt service coverage ratio
        irr: Internal rate of return
        bedrooms: Number of bedrooms
        legal_rent_compliant: Whether rent complies with encadrement

    Returns:
        StrategyFit: Strategy fit with score and reasons
    """
    pros = []
    cons = []
    reasons = []

    # Score components
    dscr_score = normalize_score(dscr, 0.8, 1.8)  # Higher DSCR potential
    irr_score = normalize_score(irr, 0.05, 0.20)  # Higher IRR potential
    bedrooms_score = normalize_score(bedrooms, 1, 5)  # More bedrooms better

    # Weighted average
    score = (dscr_score * 0.4 + irr_score * 0.4 + bedrooms_score * 0.2)

    # Penalty for insufficient bedrooms
    if bedrooms < 2:
        score *= 0.3  # 70% penalty - colocation needs multiple bedrooms
        cons.append("Insufficient bedrooms for colocation")
        reasons.append("Not suitable for flatsharing")

    # Pros/Cons
    if bedrooms >= 3:
        pros.append(f"{bedrooms} bedrooms ideal for colocation")
        reasons.append("Multiple-room premium")

    if dscr > 1.4:
        pros.append(f"Excellent cash flow (DSCR: {dscr:.2f})")
        reasons.append("Room-by-room rents boost income")
    elif dscr < 1.0:
        cons.append(f"Negative cash flow (DSCR: {dscr:.2f})")

    if irr > 0.15:
        pros.append(f"Exceptional IRR: {irr*100:.1f}%")
        reasons.append("Maximum revenue optimization")

    pros.append("Rent per room typically exceeds whole-unit rent")
    pros.append("Risk diversification across multiple tenants")

    cons.append("Complex management (multiple leases)")
    cons.append("Higher turnover and vacancy coordination")
    cons.append("Tenant compatibility issues")
    cons.append("Furnished requirements increase upfront costs")

    if not legal_rent_compliant:
        cons.append("Room rents may exceed encadrement limits")

    return StrategyFit(
        strategy="Colocation",
        score=score,
        reasons=reasons,
        pros=pros,
        cons=cons
    )


def calculate_value_add_fit(
    dscr: float,
    irr: float,
    price_discount_pct: float,
    dpe_grade: str
) -> StrategyFit:
    """
    Calculate fit score for value-add / déficit foncier strategy.

    Args:
        dscr: Debt service coverage ratio
        irr: Internal rate of return
        price_discount_pct: Discount vs median
        dpe_grade: DPE energy grade

    Returns:
        StrategyFit: Strategy fit with score and reasons
    """
    pros = []
    cons = []
    reasons = []

    # Score components
    discount_score = normalize_score(-price_discount_pct, -0.30, 0.0)  # Bigger discount better
    irr_score = normalize_score(irr, 0.08, 0.25)  # Higher IRR potential post-renovation
    dpe_score = 100 if dpe_grade in ["E", "F", "G"] else 50  # Poor DPE = value-add opportunity

    # Weighted average
    score = (discount_score * 0.4 + irr_score * 0.3 + dpe_score * 0.3)

    # Pros/Cons
    if price_discount_pct < -0.10:
        pros.append(f"Significant discount: {abs(price_discount_pct)*100:.0f}%")
        reasons.append("Below-market acquisition")

    if dpe_grade in ["E", "F", "G"]:
        pros.append(f"DPE {dpe_grade}: Major energy upgrade potential")
        reasons.append("Renovation value-add opportunity")
    else:
        cons.append(f"DPE {dpe_grade}: Limited energy upgrade value")

    if irr > 0.15:
        pros.append(f"High IRR post-renovation: {irr*100:.1f}%")
        reasons.append("Strong value creation potential")

    pros.append("Déficit foncier: Deduct renovation costs from income")
    pros.append("Post-renovation: Higher rents and property value")
    pros.append("Forced appreciation through improvements")

    cons.append("Requires upfront capital for renovations")
    cons.append("Construction risk and timeline uncertainty")
    cons.append("No rental income during works")
    cons.append("Requires project management expertise")

    return StrategyFit(
        strategy="Value-Add / déficit foncier",
        score=score,
        reasons=reasons,
        pros=pros,
        cons=cons
    )


def calculate_all_strategy_fits(
    tmc: float,
    market_rent: float,
    dscr: float,
    irr: float,
    price_discount_pct: float,
    legal_rent_compliant: bool,
    bedrooms: int,
    dpe_grade: str
) -> List[StrategyFit]:
    """
    Calculate fit scores for all strategies and return sorted by score.

    Args:
        tmc: Total monthly cost
        market_rent: Market rent
        dscr: Debt service coverage ratio
        irr: Internal rate of return
        price_discount_pct: Price discount vs median
        legal_rent_compliant: Legal rent compliance
        bedrooms: Number of bedrooms
        dpe_grade: DPE energy grade

    Returns:
        List[StrategyFit]: List of strategy fits sorted by score (best first)
    """
    strategies = [
        calculate_owner_occupier_fit(tmc, market_rent, dscr, price_discount_pct, legal_rent_compliant),
        calculate_location_nue_fit(dscr, irr, legal_rent_compliant, bedrooms),
        calculate_lmnp_fit(dscr, irr, legal_rent_compliant, bedrooms),
        calculate_colocation_fit(dscr, irr, bedrooms, legal_rent_compliant),
        calculate_value_add_fit(dscr, irr, price_discount_pct, dpe_grade)
    ]

    # Sort by score descending
    return sorted(strategies, key=lambda x: x.score, reverse=True)