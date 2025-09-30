"""
Unit tests for backend/calculations/mortgage.py
"""

import pytest
from backend.calculations import mortgage


class TestMonthlyPayment:
    """Tests for monthly_payment()"""

    def test_expected_use(self):
        """Test with typical 20-year mortgage at 3%."""
        principal = 400000
        annual_rate = 0.03
        years = 20
        result = mortgage.monthly_payment(principal, annual_rate, years)
        # Expected: ~2,219 EUR/month
        assert result == pytest.approx(2219, rel=0.01)

    def test_zero_interest(self):
        """Test with 0% interest rate."""
        principal = 400000
        annual_rate = 0.0
        years = 20
        result = mortgage.monthly_payment(principal, annual_rate, years)
        # Simple division: 400000 / (20 * 12) = 1666.67
        assert result == pytest.approx(1666.67, rel=0.01)

    def test_high_interest(self):
        """Test with high interest rate (10%)."""
        principal = 400000
        annual_rate = 0.10
        years = 20
        result = mortgage.monthly_payment(principal, annual_rate, years)
        # Expected: ~3,862 EUR/month
        assert result == pytest.approx(3862, rel=0.01)

    def test_short_term(self):
        """Test with short loan term (5 years)."""
        principal = 400000
        annual_rate = 0.03
        years = 5
        result = mortgage.monthly_payment(principal, annual_rate, years)
        # Expected: ~7,184 EUR/month
        assert result == pytest.approx(7184, rel=0.01)


class TestAmortizationSchedule:
    """Tests for amortization_schedule()"""

    def test_expected_use(self):
        """Test amortization schedule structure."""
        principal = 100000
        annual_rate = 0.03
        years = 5
        schedule = mortgage.amortization_schedule(principal, annual_rate, years)

        # Check structure
        assert len(schedule) == 60  # 5 years * 12 months
        assert all('month' in entry for entry in schedule)
        assert all('payment' in entry for entry in schedule)
        assert all('principal' in entry for entry in schedule)
        assert all('interest' in entry for entry in schedule)
        assert all('balance' in entry for entry in schedule)

    def test_first_payment_structure(self):
        """Test first payment details."""
        schedule = mortgage.amortization_schedule(100000, 0.03, 5)
        first_payment = schedule[0]

        assert first_payment['month'] == 1
        assert first_payment['payment'] == pytest.approx(first_payment['principal'] + first_payment['interest'], rel=0.01)
        assert first_payment['balance'] < 100000

    def test_final_payment_balance(self):
        """Test that final balance is approximately zero."""
        schedule = mortgage.amortization_schedule(100000, 0.03, 5)
        final_payment = schedule[-1]

        assert final_payment['month'] == 60
        assert final_payment['balance'] == pytest.approx(0, abs=1)  # Within 1 EUR

    def test_principal_increases_over_time(self):
        """Test that principal portion increases over time."""
        schedule = mortgage.amortization_schedule(100000, 0.03, 10)

        first_principal = schedule[0]['principal']
        mid_principal = schedule[60]['principal']  # Middle of loan
        last_principal = schedule[-1]['principal']

        assert first_principal < mid_principal < last_principal

    def test_interest_decreases_over_time(self):
        """Test that interest portion decreases over time."""
        schedule = mortgage.amortization_schedule(100000, 0.03, 10)

        first_interest = schedule[0]['interest']
        mid_interest = schedule[60]['interest']
        last_interest = schedule[-1]['interest']

        assert first_interest > mid_interest > last_interest