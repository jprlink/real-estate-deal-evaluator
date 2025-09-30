"""
Unit tests for backend/calculations/financial.py
"""

import pytest
from backend.calculations import financial


class TestGrossMonthlyIncome:
    """Tests for gross_monthly_income()"""

    def test_expected_use(self):
        """Test with typical monthly rent."""
        result = financial.gross_monthly_income(2000)
        assert result == 2000

    def test_zero_rent(self):
        """Test with zero rent."""
        result = financial.gross_monthly_income(0)
        assert result == 0

    def test_high_rent(self):
        """Test with very high rent."""
        result = financial.gross_monthly_income(10000)
        assert result == 10000


class TestVacancyCreditLoss:
    """Tests for vacancy_credit_loss()"""

    def test_expected_use(self):
        """Test with 5% vacancy rate."""
        gmi = 2000
        result = financial.vacancy_credit_loss(gmi, 0.05)
        assert result == 100  # 2000 * 0.05

    def test_zero_vacancy(self):
        """Test with 0% vacancy rate."""
        result = financial.vacancy_credit_loss(2000, 0.0)
        assert result == 0

    def test_high_vacancy(self):
        """Test with 20% vacancy rate."""
        result = financial.vacancy_credit_loss(2000, 0.20)
        assert result == 400


class TestNOICalculation:
    """Tests for noi_calculation()"""

    def test_expected_use(self):
        """Test with typical values."""
        gmi = 2000
        vcl = 100
        annual_oe = 6000
        result = financial.noi_calculation(gmi, vcl, annual_oe)
        # (2000 - 100) * 12 - 6000 = 1900 * 12 - 6000 = 22800 - 6000 = 16800
        assert result == 16800

    def test_negative_noi(self):
        """Test case where expenses exceed income."""
        gmi = 500
        vcl = 25
        annual_oe = 10000
        result = financial.noi_calculation(gmi, vcl, annual_oe)
        # (500 - 25) * 12 - 10000 = 475 * 12 - 10000 = 5700 - 10000 = -4300
        assert result == -4300

    def test_zero_expenses(self):
        """Test with zero operating expenses."""
        result = financial.noi_calculation(2000, 100, 0)
        assert result == 22800


class TestAnnualDebtService:
    """Tests for annual_debt_service()"""

    def test_expected_use(self):
        """Test with typical monthly payment."""
        monthly_payment = 2000
        result = financial.annual_debt_service(monthly_payment)
        assert result == 24000

    def test_zero_payment(self):
        """Test with zero monthly payment (no loan)."""
        result = financial.annual_debt_service(0)
        assert result == 0


class TestDSCRCalculation:
    """Tests for dscr_calculation()"""

    def test_positive_cash_flow(self):
        """Test with NOI > ADS (positive cash flow)."""
        noi = 20000
        ads = 15000
        result = financial.dscr_calculation(noi, ads)
        assert result == pytest.approx(1.333, rel=0.01)

    def test_break_even(self):
        """Test with NOI = ADS (break-even)."""
        result = financial.dscr_calculation(20000, 20000)
        assert result == 1.0

    def test_negative_cash_flow(self):
        """Test with NOI < ADS (negative cash flow)."""
        result = financial.dscr_calculation(15000, 20000)
        assert result == 0.75

    def test_zero_ads(self):
        """Test with zero debt service (all cash purchase)."""
        result = financial.dscr_calculation(20000, 0)
        assert result == float('inf')

    def test_negative_noi_zero_ads(self):
        """Test edge case: negative NOI with zero ADS."""
        result = financial.dscr_calculation(-5000, 0)
        assert result == 0.0


class TestCapRate:
    """Tests for cap_rate()"""

    def test_expected_use(self):
        """Test with typical values."""
        noi = 20000
        purchase_price = 500000
        result = financial.cap_rate(noi, purchase_price)
        assert result == pytest.approx(0.04, rel=0.001)  # 4%

    def test_high_cap_rate(self):
        """Test with high cap rate property."""
        result = financial.cap_rate(50000, 500000)
        assert result == pytest.approx(0.10, rel=0.001)  # 10%

    def test_zero_price(self):
        """Test with zero purchase price."""
        result = financial.cap_rate(20000, 0)
        assert result == 0.0


class TestCashOnCash:
    """Tests for cash_on_cash()"""

    def test_positive_return(self):
        """Test with positive pre-tax cash flow."""
        annual_pretax_cf = 5000
        total_cash_invested = 100000
        result = financial.cash_on_cash(annual_pretax_cf, total_cash_invested)
        assert result == pytest.approx(0.05, rel=0.001)  # 5%

    def test_negative_return(self):
        """Test with negative cash flow."""
        result = financial.cash_on_cash(-2000, 100000)
        assert result == pytest.approx(-0.02, rel=0.001)  # -2%

    def test_zero_investment(self):
        """Test with zero investment."""
        result = financial.cash_on_cash(5000, 0)
        assert result == 0.0


class TestTotalMonthlyCost:
    """Tests for total_monthly_cost()"""

    def test_expected_use(self):
        """Test with typical values."""
        monthly_payment = 2000
        monthly_charges = 200
        monthly_tax = 100
        result = financial.total_monthly_cost(monthly_payment, monthly_charges, monthly_tax)
        assert result == 2300

    def test_zero_charges(self):
        """Test with zero charges and taxes."""
        result = financial.total_monthly_cost(2000, 0, 0)
        assert result == 2000


class TestPriceToRentRatio:
    """Tests for price_to_rent_ratio()"""

    def test_expected_use(self):
        """Test with typical Paris property."""
        purchase_price = 500000
        annual_rent = 24000
        result = financial.price_to_rent_ratio(purchase_price, annual_rent)
        assert result == pytest.approx(20.83, rel=0.01)

    def test_zero_rent(self):
        """Test with zero annual rent."""
        result = financial.price_to_rent_ratio(500000, 0)
        assert result == float('inf')  # Returns infinity when rent is zero


class TestLTVRatio:
    """Tests for ltv_ratio()"""

    def test_expected_use(self):
        """Test with 80% LTV."""
        loan_amount = 400000
        property_value = 500000
        result = financial.ltv_ratio(loan_amount, property_value)
        assert result == pytest.approx(0.80, rel=0.001)

    def test_zero_property_value(self):
        """Test with zero property value."""
        result = financial.ltv_ratio(400000, 0)
        assert result == 0.0

    def test_100_percent_ltv(self):
        """Test with 100% LTV (no down payment)."""
        result = financial.ltv_ratio(500000, 500000)
        assert result == 1.0