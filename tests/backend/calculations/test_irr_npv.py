"""
Unit tests for backend/calculations/irr_npv.py
"""

import pytest
from backend.calculations import irr_npv


class TestIRRCalculation:
    """Tests for irr_calculation()"""

    def test_positive_irr(self, sample_cash_flows):
        """Test with positive cash flows."""
        result = irr_npv.irr_calculation(sample_cash_flows)
        # Expected IRR should be around 10-12%
        assert 0.10 <= result <= 0.15

    def test_zero_irr(self):
        """Test with break-even cash flows."""
        cash_flows = [-100000, 10000, 10000, 10000, 10000, 10000,
                      10000, 10000, 10000, 10000, 10000]
        result = irr_npv.irr_calculation(cash_flows)
        # Break-even IRR should be close to 0%
        assert result == pytest.approx(0.0, abs=0.01)

    def test_negative_irr(self):
        """Test with negative cash flows (bad investment)."""
        cash_flows = [-100000, 5000, 5000, 5000, 5000, 5000]
        result = irr_npv.irr_calculation(cash_flows)
        # Loss scenario
        assert result < 0


class TestNPVCalculation:
    """Tests for npv_calculation()"""

    def test_positive_npv(self, sample_cash_flows):
        """Test with positive NPV at 8% discount rate."""
        discount_rate = 0.08
        result = irr_npv.npv_calculation(discount_rate, sample_cash_flows)
        assert result > 0

    def test_negative_npv(self):
        """Test with high discount rate resulting in negative NPV."""
        cash_flows = [-100000, 10000, 10000, 10000, 10000, 10000]
        discount_rate = 0.20  # High discount rate
        result = irr_npv.npv_calculation(discount_rate, cash_flows)
        assert result < 0

    def test_zero_discount_rate(self, sample_cash_flows):
        """Test with 0% discount rate (sum of cash flows)."""
        result = irr_npv.npv_calculation(0.0, sample_cash_flows)
        # At 0% discount, NPV = sum of all cash flows
        expected = sum(sample_cash_flows)
        assert result == pytest.approx(expected, rel=0.01)


class TestNetSaleProceeds:
    """Tests for net_sale_proceeds()"""

    def test_expected_use(self):
        """Test with typical values."""
        sale_price = 600000
        selling_costs = 30000
        remaining_mortgage = 300000
        result = irr_npv.net_sale_proceeds(sale_price, selling_costs, remaining_mortgage)
        # 600000 - 30000 - 300000 = 270000
        assert result == 270000

    def test_zero_mortgage(self):
        """Test with paid-off mortgage."""
        result = irr_npv.net_sale_proceeds(600000, 30000, 0)
        assert result == 570000

    def test_negative_proceeds(self):
        """Test with sale price less than costs + mortgage."""
        result = irr_npv.net_sale_proceeds(400000, 30000, 400000)
        # 400000 - 30000 - 400000 = -30000
        assert result == -30000


class TestEquityMultiple:
    """Tests for equity_multiple()"""

    def test_expected_use(self):
        """Test with typical property investment."""
        total_cash_returned = 150000
        total_cash_invested = 100000
        result = irr_npv.equity_multiple(total_cash_returned, total_cash_invested)
        assert result == 1.5

    def test_break_even(self):
        """Test with break-even scenario."""
        result = irr_npv.equity_multiple(100000, 100000)
        assert result == 1.0

    def test_loss(self):
        """Test with loss scenario."""
        result = irr_npv.equity_multiple(80000, 100000)
        assert result == 0.8

    def test_zero_investment(self):
        """Test with zero investment."""
        result = irr_npv.equity_multiple(150000, 0)
        assert result == 0.0