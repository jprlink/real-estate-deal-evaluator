"""
Unit tests for backend/calculations/valuation.py
"""

import pytest
from backend.calculations import valuation


class TestNowcastValue:
    """Tests for nowcast_value()"""

    def test_expected_use(self):
        """Test with typical market adjustments."""
        dvf_median = 10000
        market_delta = 0.05  # Market up 5%
        listing_delta = 0.03  # Listings up 3%

        result = valuation.nowcast_value(dvf_median, market_delta, listing_delta)
        # 10000 * 1.05 * 1.03 = 10815
        assert result == pytest.approx(10815, rel=0.01)

    def test_no_adjustments(self):
        """Test with zero deltas."""
        result = valuation.nowcast_value(10000, 0.0, 0.0)
        assert result == 10000

    def test_negative_market(self):
        """Test with declining market."""
        result = valuation.nowcast_value(10000, -0.10, -0.05)
        # 10000 * 0.90 * 0.95 = 8550
        assert result == pytest.approx(8550, rel=0.01)


class TestPriceVerdict:
    """Tests for price_verdict()"""

    def test_underpriced(self):
        """Test property priced below market."""
        property_price_per_m2 = 9000
        nowcast_value_per_m2 = 10000
        result = valuation.price_verdict(property_price_per_m2, nowcast_value_per_m2)
        # 9000 / 10000 = 0.90 < 0.95
        assert result == "Under-priced"

    def test_average_price(self):
        """Test property priced at market."""
        result = valuation.price_verdict(10000, 10000)
        # Ratio = 1.0, within 0.95-1.05 range
        assert result == "Average"

    def test_overpriced(self):
        """Test property priced above market."""
        property_price_per_m2 = 11000
        nowcast_value_per_m2 = 10000
        result = valuation.price_verdict(property_price_per_m2, nowcast_value_per_m2)
        # 11000 / 10000 = 1.10 > 1.05
        assert result == "Overpriced"

    def test_edge_case_lower(self):
        """Test edge case at 95% threshold."""
        result = valuation.price_verdict(9500, 10000)
        # Ratio = 0.95, should be "Average"
        assert result == "Average"

    def test_edge_case_upper(self):
        """Test edge case at 105% threshold."""
        result = valuation.price_verdict(10500, 10000)
        # Ratio = 1.05, should be "Average"
        assert result == "Average"


class TestListingDelta:
    """Tests for listing_delta()"""

    def test_above_median(self):
        """Test listing priced above median."""
        property_price = 550000
        dvf_median = 500000
        result = valuation.listing_delta(property_price, dvf_median)
        # (550000 - 500000) / 500000 = 0.10
        assert result == pytest.approx(0.10, rel=0.001)

    def test_at_median(self):
        """Test listing priced at median."""
        result = valuation.listing_delta(500000, 500000)
        assert result == 0.0

    def test_below_median(self):
        """Test listing priced below median."""
        result = valuation.listing_delta(450000, 500000)
        # (450000 - 500000) / 500000 = -0.10
        assert result == pytest.approx(-0.10, rel=0.001)

    def test_zero_median(self):
        """Test with zero median (edge case)."""
        result = valuation.listing_delta(500000, 0)
        assert result == 0.0


class TestYieldOnCost:
    """Tests for yield_on_cost()"""

    def test_expected_use(self):
        """Test with typical rental property."""
        noi = 20000
        total_investment = 500000
        result = valuation.yield_on_cost(noi, total_investment)
        # 20000 / 500000 = 0.04 (4%)
        assert result == pytest.approx(0.04, rel=0.001)

    def test_high_yield(self):
        """Test with high-yield property."""
        result = valuation.yield_on_cost(50000, 500000)
        # 50000 / 500000 = 0.10 (10%)
        assert result == pytest.approx(0.10, rel=0.001)

    def test_negative_noi(self):
        """Test with negative NOI."""
        result = valuation.yield_on_cost(-10000, 500000)
        # -10000 / 500000 = -0.02 (-2%)
        assert result == pytest.approx(-0.02, rel=0.001)

    def test_zero_investment(self):
        """Test with zero total investment."""
        result = valuation.yield_on_cost(20000, 0)
        assert result == 0.0