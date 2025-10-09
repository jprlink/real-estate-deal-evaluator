"""
Unit tests for cash flow calculations.
"""

import pytest
from backend.calculations.cashflow import (
    calculate_cash_flow_projection,
    calculate_total_return_with_sale,
    CashFlowProjection
)
from backend.calculations.mortgage import amortization_schedule


def test_cash_flow_projection_basic():
    """Test basic cash flow projection calculation."""
    # Simple scenario: 500k property, 2500/month rent
    schedule = amortization_schedule(
        principal=400000,
        annual_rate=0.035,
        years=20
    )

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=10
    )

    assert len(projections) == 10
    assert all(isinstance(p, CashFlowProjection) for p in projections)


def test_cash_flow_projection_year_1():
    """Test Year 1 cash flow calculations."""
    schedule = amortization_schedule(400000, 0.035, 20)

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=10
    )

    year1 = projections[0]

    # Year 1 checks
    assert year1.year == 1
    assert year1.rental_income == pytest.approx(2500 * 12, rel=0.01)
    assert year1.operating_expenses == pytest.approx(600 * 12, rel=0.01)
    assert year1.mortgage_payment == pytest.approx(2317.30 * 12, rel=0.01)
    assert year1.noi == pytest.approx((2500 - 600) * 12, rel=0.01)
    assert year1.cash_flow == year1.noi - year1.mortgage_payment
    assert year1.cumulative_cash_flow == year1.cash_flow


def test_cash_flow_projection_appreciation():
    """Test property appreciation over time."""
    schedule = amortization_schedule(400000, 0.035, 20)

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.03,  # 3% per year
        years=5
    )

    # Property value should increase each year
    for i in range(1, len(projections)):
        assert projections[i].property_value > projections[i-1].property_value

    # Year 5 value should be approximately initial * (1.03)^5
    expected_year5 = 500000 * (1.03 ** 5)
    assert projections[4].property_value == pytest.approx(expected_year5, rel=0.01)


def test_cash_flow_projection_equity_growth():
    """Test equity growth over time."""
    schedule = amortization_schedule(400000, 0.035, 20)

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=10
    )

    # Equity should increase each year (appreciation + principal paydown)
    for i in range(1, len(projections)):
        assert projections[i].equity > projections[i-1].equity


def test_cash_flow_projection_cumulative():
    """Test cumulative cash flow calculation."""
    schedule = amortization_schedule(400000, 0.035, 20)

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=3
    )

    # Cumulative should be sum of all previous years
    assert projections[0].cumulative_cash_flow == projections[0].cash_flow
    assert projections[1].cumulative_cash_flow == pytest.approx(
        projections[0].cash_flow + projections[1].cash_flow, rel=0.01
    )
    assert projections[2].cumulative_cash_flow == pytest.approx(
        projections[0].cash_flow + projections[1].cash_flow + projections[2].cash_flow,
        rel=0.01
    )


def test_cash_flow_projection_negative_appreciation():
    """Test cash flow with negative appreciation (market correction)."""
    schedule = amortization_schedule(400000, 0.035, 20)

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=-0.02,  # -2% per year (correction)
        years=5
    )

    # Property value should decrease each year
    for i in range(1, len(projections)):
        assert projections[i].property_value < projections[i-1].property_value


def test_total_return_with_sale():
    """Test total return calculation including property sale."""
    schedule = amortization_schedule(400000, 0.035, 20)

    projections = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2500,
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=10
    )

    result = calculate_total_return_with_sale(
        projections=projections,
        initial_equity=100000,
        selling_costs_rate=0.08
    )

    assert "final_property_value" in result
    assert "selling_costs" in result
    assert "net_sale_proceeds" in result
    assert "total_return" in result
    assert "total_return_on_equity" in result

    # Selling costs should be 8% of final value
    assert result["selling_costs"] == pytest.approx(
        result["final_property_value"] * 0.08, rel=0.01
    )

    # Net proceeds = value - costs - remaining balance
    assert result["net_sale_proceeds"] == pytest.approx(
        result["final_property_value"] -
        result["selling_costs"] -
        result["remaining_loan_balance"],
        rel=0.01
    )


def test_total_return_empty_projections():
    """Test total return with empty projections."""
    result = calculate_total_return_with_sale(
        projections=[],
        initial_equity=100000,
        selling_costs_rate=0.08
    )

    assert result["total_return"] == 0.0
    assert result["total_return_on_equity"] == 0.0


def test_cash_flow_positive_vs_negative():
    """Test positive vs negative cash flow scenarios."""
    schedule = amortization_schedule(400000, 0.035, 20)

    # Positive cash flow scenario (higher rent)
    projections_positive = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=3000,  # Higher rent
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=5
    )

    # Negative cash flow scenario (lower rent)
    projections_negative = calculate_cash_flow_projection(
        initial_property_value=500000,
        monthly_rent=2000,  # Lower rent
        monthly_operating_expenses=600,
        monthly_mortgage_payment=2317.30,
        loan_amortization_schedule=schedule,
        appreciation_rate=0.02,
        years=5
    )

    assert projections_positive[0].cash_flow > 0
    assert projections_negative[0].cash_flow < 0
