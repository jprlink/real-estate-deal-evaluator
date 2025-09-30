"""
Property evaluation API endpoints.
"""

from fastapi import APIRouter, HTTPException
from backend.api.schemas import PropertyEvaluationRequest, PropertyEvaluationResponse, FinancialMetrics, StrategyFit
from backend.calculations import financial, mortgage, strategy_fit
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

        # Calculate financial metrics
        gmi = financial.gross_monthly_income(request.monthly_rent)
        vcl = financial.vacancy_credit_loss(gmi, 0.05)  # 5% vacancy rate
        annual_oe = 6000  # Placeholder operating expenses
        noi = financial.noi_calculation(gmi, vcl, annual_oe)

        ads = financial.annual_debt_service(monthly_payment)
        dscr = financial.dscr_calculation(noi, ads)

        cap_rate = financial.cap_rate(noi, request.price)

        annual_pretax_cf = noi - ads
        coc = financial.cash_on_cash(annual_pretax_cf, request.down_payment)

        price_per_m2 = request.price / request.surface
        ltv = financial.ltv_ratio(request.loan_amount, request.price)

        # Simple IRR calculation (placeholder - would use full cash flow analysis)
        # For now, approximate with cash-on-cash
        estimated_irr = coc * 0.8  # Rough approximation

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

        # Legal rent status (simplified - would use actual rent control data)
        rent_per_m2 = request.monthly_rent / request.surface
        if rent_per_m2 < 30:
            legal_rent_status = "Conformant – Low"
        elif rent_per_m2 <= 35:
            legal_rent_status = "Conformant – High"
        else:
            legal_rent_status = "Non-conformant"

        # Build response
        metrics = FinancialMetrics(
            monthly_payment=monthly_payment,
            noi=noi,
            dscr=dscr,
            cap_rate=cap_rate,
            cash_on_cash=coc,
            irr=estimated_irr,
            price_per_m2=price_per_m2,
            ltv=ltv
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
            summary=summary
        )

    except Exception as e:
        logger.error(f"Error evaluating property: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")