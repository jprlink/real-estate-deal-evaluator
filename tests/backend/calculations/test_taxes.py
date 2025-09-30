"""
Unit tests for backend/calculations/taxes.py
"""

import pytest
from backend.calculations import taxes


class TestLMNPMicroBIC:
    """Tests for lmnp_micro_bic_tax()"""

    def test_expected_use(self):
        """Test with typical LMNP rental income."""
        gross_annual_rent = 24000
        abatement_rate = 0.50
        marginal_rate = 0.30
        social_charges = 0.172

        result = taxes.lmnp_micro_bic_tax(gross_annual_rent, abatement_rate, marginal_rate, social_charges)

        # Taxable = 24000 * (1 - 0.50) = 12000
        # Income tax = 12000 * 0.30 = 3600
        # Social charges = 12000 * 0.172 = 2064
        # Total = 3600 + 2064 = 5664
        assert result['taxable_income'] == 12000
        assert result['income_tax'] == 3600
        assert result['social_charges'] == 2064
        assert result['total_tax'] == 5664

    def test_zero_rent(self):
        """Test with zero rental income."""
        result = taxes.lmnp_micro_bic_tax(0, 0.50, 0.30, 0.172)
        assert result['total_tax'] == 0

    def test_no_abatement(self):
        """Test with 0% abatement."""
        result = taxes.lmnp_micro_bic_tax(24000, 0.0, 0.30, 0.172)
        # Full amount is taxable
        assert result['taxable_income'] == 24000


class TestLocationNueMicroFoncier:
    """Tests for location_nue_micro_foncier_tax()"""

    def test_expected_use(self):
        """Test with typical unfurnished rental income."""
        gross_annual_rent = 20000
        abatement_rate = 0.30
        marginal_rate = 0.30
        social_charges = 0.172

        result = taxes.location_nue_micro_foncier_tax(gross_annual_rent, abatement_rate, marginal_rate, social_charges)

        # Taxable = 20000 * (1 - 0.30) = 14000
        # Income tax = 14000 * 0.30 = 4200
        # Social charges = 14000 * 0.172 = 2408
        # Total = 4200 + 2408 = 6608
        assert result['taxable_income'] == 14000
        assert result['income_tax'] == 4200
        assert result['social_charges'] == 2408
        assert result['total_tax'] == 6608

    def test_higher_abatement(self):
        """Test with higher abatement rate."""
        result = taxes.location_nue_micro_foncier_tax(20000, 0.50, 0.30, 0.172)
        # Taxable = 20000 * 0.50 = 10000
        assert result['taxable_income'] == 10000


class TestRegimeReelTax:
    """Tests for regime_reel_tax()"""

    def test_positive_income(self):
        """Test with positive net rental income."""
        gross_annual_rent = 24000
        deductible_expenses = 8000
        mortgage_interest = 4000
        marginal_rate = 0.30
        social_charges = 0.172

        result = taxes.regime_reel_tax(gross_annual_rent, deductible_expenses, mortgage_interest, marginal_rate, social_charges)

        # Net rental income = 24000 - 8000 - 4000 = 12000
        # Income tax = 12000 * 0.30 = 3600
        # Social charges = 12000 * 0.172 = 2064
        # Total = 3600 + 2064 = 5664
        assert result['net_rental_income'] == 12000
        assert result['income_tax'] == 3600
        assert result['social_charges'] == 2064
        assert result['total_tax'] == 5664

    def test_deficit_foncier(self):
        """Test with déficit foncier (expenses > income)."""
        gross_annual_rent = 15000
        deductible_expenses = 12000
        mortgage_interest = 8000
        marginal_rate = 0.30
        social_charges = 0.172

        result = taxes.regime_reel_tax(gross_annual_rent, deductible_expenses, mortgage_interest, marginal_rate, social_charges)

        # Net rental income = 15000 - 12000 - 8000 = -5000 (deficit)
        # No tax on deficit
        assert result['net_rental_income'] == -5000
        assert result['income_tax'] == 0
        assert result['social_charges'] == 0
        assert result['total_tax'] == 0

    def test_zero_expenses(self):
        """Test with no deductible expenses."""
        result = taxes.regime_reel_tax(24000, 0, 0, 0.30, 0.172)
        # Full rent is taxable
        assert result['net_rental_income'] == 24000