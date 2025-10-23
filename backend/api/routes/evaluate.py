"""
Property evaluation API endpoints.
"""

from fastapi import APIRouter, HTTPException
from backend.api.schemas import (PropertyEvaluationRequest, PropertyEvaluationResponse,
                                FinancialMetrics, StrategyFit, CashFlowYear, RentBand, PurchaseCosts)
from backend.calculations import financial, mortgage, strategy_fit, cashflow
from backend.data import appreciation_rates, postal_codes, rent_control
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/evaluate", response_model=PropertyEvaluationResponse)
async def evaluate_property(request: PropertyEvaluationRequest):
    """
    Evaluate a property investment opportunity.

    Returns:
        PropertyEvaluationResponse: Complete evaluation with verdict, metrics, and strategy fits
    """
    try:
        # Calculate mortgage payment
        monthly_payment = mortgage.monthly_payment(
            principal=request.loan_amount,
            annual_rate=request.annual_rate,
            years=request.loan_term
        )

        # Estimate monthly operating expenses (property tax, insurance, maintenance, HOA)
        # Typical: 20-30% of rental income, using 25%
        monthly_opex = request.monthly_rent * 0.25
        annual_oe = monthly_opex * 12

        # Calculate financial metrics
        gmi = financial.gross_monthly_income(request.monthly_rent)
        vcl = financial.vacancy_credit_loss(gmi, 0.05)  # 5% vacancy rate
        noi = financial.noi_calculation(gmi, vcl, annual_oe)

        ads = financial.annual_debt_service(monthly_payment)
        dscr = financial.dscr_calculation(noi, ads)

        cap_rate = financial.cap_rate(noi, request.price)

        annual_pretax_cf = noi - ads
        coc = financial.cash_on_cash(annual_pretax_cf, request.down_payment)

        price_per_m2 = request.price / request.surface
        ltv = financial.ltv_ratio(request.loan_amount, request.price)

        # Get appreciation rate for the postal code
        appreciation_rate = appreciation_rates.get_appreciation_rate(
            postal_code=request.postal_code,
            forward_looking=True
        )
        appreciation_rate_display = appreciation_rates.get_appreciation_rate_display(
            postal_code=request.postal_code,
            forward_looking=True
        )
        appreciation_source = appreciation_rates.get_appreciation_source()

        # Calculate amortization schedule for cash flow projections
        amortization_schedule = mortgage.amortization_schedule(
            principal=request.loan_amount,
            annual_rate=request.annual_rate,
            years=request.loan_term
        )

        # Calculate detailed purchase costs BEFORE cashflow projection
        purchase_price = request.price
        has_mortgage = request.loan_amount > 0
        costs_breakdown = cashflow.calculate_french_purchase_costs(purchase_price, has_mortgage)
        total_purchase_fees = costs_breakdown["total"]

        # Calculate cash flow projections with appreciation (user-defined years)
        # Use same vacancy rate as DSCR calculation for consistency
        VACANCY_RATE = 0.05  # 5% vacancy & credit loss

        # Include renovation costs in total property value
        total_property_value = request.price + request.renovation_costs

        projections = cashflow.calculate_cash_flow_projection(
            initial_property_value=total_property_value,
            monthly_rent=request.monthly_rent,
            monthly_operating_expenses=monthly_opex,
            monthly_mortgage_payment=monthly_payment,
            loan_amortization_schedule=amortization_schedule,
            appreciation_rate=appreciation_rate,
            vacancy_rate=VACANCY_RATE,
            years=request.projection_years,
            down_payment=request.down_payment,
            renovation_costs=request.renovation_costs,
            purchase_fees=total_purchase_fees
        )

        # Calculate IRR from actual cash flows
        # Note: projections already include Year 0 with all purchase costs
        cash_flows = [p.cash_flow for p in projections]

        # Add sale proceeds to final year
        # Total cash required = down payment + renovation + all purchase fees
        total_cash_required = request.down_payment + request.renovation_costs + total_purchase_fees

        sale_result = cashflow.calculate_total_return_with_sale(
            projections=projections,
            initial_equity=total_cash_required,
            selling_costs_rate=0.08
        )
        cash_flows[-1] += sale_result["net_sale_proceeds"]

        # Calculate IRR from cash flows
        from backend.calculations.irr_npv import irr_calculation
        estimated_irr = irr_calculation(cash_flows)
        if estimated_irr != estimated_irr:  # Check for NaN
            estimated_irr = coc * 0.8  # Fallback to approximation

        # Convert projections to response format
        cash_flow_years = [
            CashFlowYear(
                year=p.year,
                rental_income=p.rental_income,
                vacancy_loss=p.vacancy_loss,
                effective_rental_income=p.effective_rental_income,
                operating_expenses=p.operating_expenses,
                mortgage_payment=p.mortgage_payment,
                noi=p.noi,
                cash_flow=p.cash_flow,
                cumulative_cash_flow=p.cumulative_cash_flow,
                property_value=p.property_value,
                equity=p.equity
            )
            for p in projections
        ]

        # Calculate strategy fits
        tmc = financial.total_monthly_cost(monthly_payment, 200, 100)  # Placeholder charges
        fits = strategy_fit.calculate_all_strategy_fits(
            tmc=tmc,
            market_rent=request.monthly_rent,
            dscr=dscr,
            irr=estimated_irr,
            price_discount_pct=0.0,  # Would come from DVF comparison
            legal_rent_compliant=True,  # Would come from rent control check
            bedrooms=request.bedrooms,
            dpe_grade=request.dpe or "D"
        )

        # Determine verdicts
        if dscr >= 1.2:
            verdict = "BUY"
        elif dscr >= 1.0:
            verdict = "CAUTION"
        else:
            verdict = "PASS"

        # Price verdict using DVF database with progressive geographic search
        from backend.integrations.dvf import (
            fetch_dvf_comps_progressive,
            calculate_weighted_median_and_bands
        )
        from datetime import datetime

        # Get detected city from postal code (needed for logging)
        detected_city = postal_codes.get_city_from_postal_code(request.postal_code)

        # Fetch comparable sales from DVF with progressive search
        # TODO: Get actual lat/lon from geocoding service or address
        dvf_comps, geo_scope = await fetch_dvf_comps_progressive(
            postal_code=request.postal_code,
            surface=request.surface,
            lat=None,  # Would come from geocoding
            lon=None,  # Would come from geocoding
            rooms=request.rooms,
            property_type="Appartement",  # TODO: Could be inferred from property characteristics
            min_comps=12
        )

        price_source = None
        if dvf_comps and len(dvf_comps) >= 12:  # Need at least 12 comps for robust statistics
            # Calculate weighted median and percentile bands
            stats = calculate_weighted_median_and_bands(
                dvf_comps,
                reference_date=datetime.now(),
                subject_rooms=request.rooms
            )

            median_market_price = stats["median"]
            p25 = stats["p25"]
            p75 = stats["p75"]
            p10 = stats["p10"]
            p90 = stats["p90"]

            # Determine price verdict based on P25-P75 band
            if price_per_m2 < p25:
                price_verdict = "Under-priced"
            elif price_per_m2 <= p75:
                price_verdict = "Fair"
            else:
                price_verdict = "Over-priced"

            # Get time range from comps
            dates = [c["date_mutation"] for c in dvf_comps if c.get("date_mutation")]
            min_date = min(dates) if dates else "N/A"
            max_date = max(dates) if dates else "N/A"

            price_source = (
                f"Based on {len(dvf_comps)} comparable sales from DVF (Demandes de Valeurs Foncières). "
                f"Geographic scope: {geo_scope}. Time range: {min_date} to {max_date}. "
                f"Weighted median: €{median_market_price:.0f}/m² (P25-P75: €{p25:.0f}-€{p75:.0f}/m²). "
                f"⚠️ DVF data last updated June 2019 (6+ years old). "
                f"Feature adjustments (elevator, balcony, DPE) not applied—data unavailable in DVF."
            )
            logger.info(f"DVF analysis: {len(dvf_comps)} comps, median €{median_market_price:.0f}/m², property €{price_per_m2:.0f}/m², scope: {geo_scope}")
        else:
            # Fallback to location-based market ranges if DVF data unavailable
            logger.warning(f"Insufficient DVF data ({len(dvf_comps)} comps), using fallback pricing for {detected_city}")

            # Department-specific fallback ranges (€/m²)
            department = request.postal_code[:2]
            fallback_ranges = {
                "75": {"low": 9500, "high": 11000, "name": "Paris"},  # Paris
                "92": {"low": 5500, "high": 7500, "name": "Hauts-de-Seine"},
                "93": {"low": 3500, "high": 5000, "name": "Seine-Saint-Denis"},
                "94": {"low": 4500, "high": 6000, "name": "Val-de-Marne"},
                "91": {"low": 3500, "high": 4500, "name": "Essonne"},
                "95": {"low": 3000, "high": 4000, "name": "Val-d'Oise"},
                "78": {"low": 3500, "high": 4500, "name": "Yvelines"},
                "77": {"low": 2500, "high": 3500, "name": "Seine-et-Marne"},
            }

            fallback = fallback_ranges.get(department, {"low": 2000, "high": 4000, "name": "France"})

            if price_per_m2 < fallback["low"]:
                price_verdict = "Under-priced"
            elif price_per_m2 <= fallback["high"]:
                price_verdict = "Average"
            else:
                price_verdict = "Overpriced"

            price_source = f"Based on typical market ranges for {fallback['name']} (€{fallback['low']:,}-€{fallback['high']:,}/m²). DVF comparable sales data not available (need 3+ recent transactions)."

        # Build purchase costs response object (costs_breakdown already calculated above)
        purchase_costs_obj = PurchaseCosts(
            down_payment=request.down_payment,
            renovation_costs=request.renovation_costs,
            registration_duties=costs_breakdown["registration_duties"],
            notaire_fees=costs_breakdown["notaire_fees"],
            disbursements=costs_breakdown["disbursements"],
            mortgage_fees=costs_breakdown["mortgage_fees"],
            total_fees=costs_breakdown["total"],
            total_cash_required=request.down_payment + request.renovation_costs + costs_breakdown["total"]
        )

        # Legal rent status using real rent control data
        rent_compliance = rent_control.check_rent_compliance(
            postal_code=request.postal_code,
            monthly_rent=request.monthly_rent,
            surface=request.surface
        )

        if rent_compliance:
            legal_rent_status = rent_compliance["verdict"]
            rent_band = RentBand(
                min_rent=rent_compliance["min_rent"],
                max_rent=rent_compliance["max_rent"],
                median_rent=rent_compliance["median_rent"],
                property_rent_per_m2=rent_compliance["property_rent_per_m2"],
                total_monthly_rent=rent_compliance["total_monthly_rent"],
                surface=rent_compliance["surface"],
                is_compliant=rent_compliance["is_compliant"],
                compliance_percentage=rent_compliance["compliance_percentage"],
                is_estimate=rent_compliance.get("is_estimate", False)
            )
        else:
            # Not in rent-controlled zone
            rent_per_m2 = request.monthly_rent / request.surface
            legal_rent_status = "No rent control in this area"
            rent_band = None

        # Build response
        metrics = FinancialMetrics(
            monthly_payment=monthly_payment,
            noi=noi,
            dscr=dscr,
            cap_rate=cap_rate,
            cash_on_cash=coc,
            irr=estimated_irr,
            price_per_m2=price_per_m2,
            ltv=ltv,
            appreciation_rate=appreciation_rate,
            appreciation_rate_display=appreciation_rate_display
        )

        strategy_fits_response = [
            StrategyFit(
                strategy=fit.strategy,
                score=fit.score,
                pros=fit.pros,
                cons=fit.cons
            )
            for fit in fits[:3]  # Top 3 strategies
        ]

        summary = f"Property at {request.address}: DSCR {dscr:.2f}, Cap Rate {cap_rate*100:.1f}%, IRR {estimated_irr*100:.1f}%. Verdict: {verdict}"

        return PropertyEvaluationResponse(
            verdict=verdict,
            price_verdict=price_verdict,
            legal_rent_status=legal_rent_status,
            metrics=metrics,
            strategy_fits=strategy_fits_response,
            summary=summary,
            cash_flow_projections=cash_flow_years,
            appreciation_source=appreciation_source,
            rent_band=rent_band,
            city=detected_city,
            price_source=price_source,
            purchase_costs=purchase_costs_obj
        )

    except Exception as e:
        logger.error(f"Error evaluating property: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")