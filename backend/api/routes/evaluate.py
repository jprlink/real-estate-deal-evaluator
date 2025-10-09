"""
Property evaluation API endpoints.
"""

from fastapi import APIRouter, HTTPException
from backend.api.schemas import (PropertyEvaluationRequest, PropertyEvaluationResponse,
                                FinancialMetrics, StrategyFit, CashFlowYear, RentBand)
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

        # Calculate cash flow projections with appreciation (user-defined years)
        projections = cashflow.calculate_cash_flow_projection(
            initial_property_value=request.price,
            monthly_rent=request.monthly_rent,
            monthly_operating_expenses=monthly_opex,
            monthly_mortgage_payment=monthly_payment,
            loan_amortization_schedule=amortization_schedule,
            appreciation_rate=appreciation_rate,
            years=request.projection_years
        )

        # Calculate IRR from actual cash flows
        initial_equity = request.down_payment
        cash_flows = [-initial_equity]  # Initial investment (negative)
        for p in projections:
            cash_flows.append(p.cash_flow)

        # Add sale proceeds to final year
        sale_result = cashflow.calculate_total_return_with_sale(
            projections=projections,
            initial_equity=initial_equity,
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

        # Price verdict (simplified - would use DVF data)
        if price_per_m2 < 9500:
            price_verdict = "Under-priced"
        elif price_per_m2 <= 11000:
            price_verdict = "Average"
        else:
            price_verdict = "Overpriced"

        # Get detected city from postal code
        detected_city = postal_codes.get_city_from_postal_code(request.postal_code)

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
            city=detected_city
        )

    except Exception as e:
        logger.error(f"Error evaluating property: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")