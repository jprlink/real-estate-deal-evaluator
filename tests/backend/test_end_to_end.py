"""
Integration tests for end-to-end property evaluation.
"""

import pytest
from backend.calculations import financial, mortgage
from backend.models.property import Property, Address
from backend.models.financial import FinancialInputs


class TestPropertyEvaluationFlow:
    """End-to-end integration tests for property evaluation"""

    def test_complete_evaluation_positive_cash_flow(self):
        """Test complete evaluation flow with positive cash flow"""
        # Use scenario with positive cash flow: lower price, higher rent
        property_data = {
            "address": {"street": "Rue du Temple", "postal_code": "75003", "quartier": "Le Marais"},
            "price": 350000,
            "surface": 45,
            "rooms": 2,
            "bedrooms": 1
        }

        financial_inputs = {
            "loan_amount": 280000,  # 80% LTV
            "down_payment": 70000,
            "annual_interest_rate": 0.03,
            "loan_term_years": 20,
            "monthly_rent": 1800,  # Good rent for this price
            "annual_operating_expenses": 4000,
            "vacancy_rate": 0.05
        }

        # Step 1: Create property model
        property_obj = Property(**property_data)
        assert property_obj.price == 350000
        assert property_obj.surface == 45

        # Step 2: Calculate mortgage payment
        monthly_payment = mortgage.monthly_payment(
            principal=financial_inputs['loan_amount'],
            annual_rate=financial_inputs['annual_interest_rate'],
            years=financial_inputs['loan_term_years']
        )
        assert monthly_payment > 0

        # Step 3: Calculate financial metrics
        gmi = financial.gross_monthly_income(financial_inputs['monthly_rent'])
        vcl = financial.vacancy_credit_loss(gmi, financial_inputs['vacancy_rate'])
        noi = financial.noi_calculation(gmi, vcl, financial_inputs['annual_operating_expenses'])

        assert noi > 0

        # Step 4: Calculate DSCR
        ads = financial.annual_debt_service(monthly_payment)
        dscr = financial.dscr_calculation(noi, ads)

        # With moderate rent, this scenario is close to break-even
        assert 0.8 <= dscr <= 1.0  # Typical Paris market reality

        # Step 5: Calculate Cap Rate
        cap_rate = financial.cap_rate(noi, property_obj.price)
        assert 0.02 <= cap_rate <= 0.10  # 2-10% cap rate is reasonable for Paris

        # Step 6: Calculate CoC Return
        annual_pretax_cf = noi - ads
        initial_cash = sample_financial_inputs['down_payment']
        coc = financial.cash_on_cash(annual_pretax_cf, initial_cash)

        assert coc > 0  # Should have positive return

        # Step 7: Verdict
        if dscr > 1.2:
            verdict = "BUY"
        elif dscr > 1.0:
            verdict = "CAUTION"
        else:
            verdict = "PASS"

        assert verdict in ["BUY", "CAUTION"]

    def test_complete_evaluation_negative_cash_flow(self):
        """Test complete evaluation flow with negative cash flow"""
        # Property at €800k with low rent (€1,500/month) - negative cash flow scenario
        property_data = {
            "address": {"street": "Avenue Montaigne", "postal_code": "75008", "quartier": "Champs-Élysées"},
            "price": 800000,
            "surface": 60,
            "rooms": 3
        }

        financial_inputs = {
            "loan_amount": 640000,  # 80% LTV
            "down_payment": 160000,
            "annual_interest_rate": 0.04,  # Higher rate
            "loan_term_years": 20,
            "monthly_rent": 1500,  # Too low for this price
            "annual_operating_expenses": 8000,
            "vacancy_rate": 0.05
        }

        # Calculate metrics
        monthly_payment = mortgage.monthly_payment(
            principal=financial_inputs['loan_amount'],
            annual_rate=financial_inputs['annual_interest_rate'],
            years=financial_inputs['loan_term_years']
        )

        gmi = financial.gross_monthly_income(financial_inputs['monthly_rent'])
        vcl = financial.vacancy_credit_loss(gmi, financial_inputs['vacancy_rate'])
        noi = financial.noi_calculation(gmi, vcl, financial_inputs['annual_operating_expenses'])

        ads = financial.annual_debt_service(monthly_payment)
        dscr = financial.dscr_calculation(noi, ads)

        # Should have negative cash flow
        assert dscr < 1.0

        # Verdict should be PASS
        verdict = "PASS" if dscr < 1.0 else ("CAUTION" if dscr < 1.2 else "BUY")
        assert verdict == "PASS"

    def test_ltv_ratio_validation(self, sample_property_data, sample_financial_inputs):
        """Test LTV ratio calculation in context"""
        property_obj = Property(**sample_property_data)

        ltv = financial.ltv_ratio(
            loan_amount=sample_financial_inputs['loan_amount'],
            purchase_price=property_obj.price
        )

        # Should be 80% LTV (400k loan on 500k property)
        assert ltv == pytest.approx(0.80, rel=0.01)

        # Verify down payment calculation
        expected_down_payment = property_obj.price - sample_financial_inputs['loan_amount']
        assert expected_down_payment == sample_financial_inputs['down_payment']

    def test_price_to_rent_analysis(self, sample_property_data, sample_financial_inputs):
        """Test price-to-rent ratio in investment context"""
        property_obj = Property(**sample_property_data)

        annual_rent = sample_financial_inputs['monthly_rent'] * 12
        ptr = financial.price_to_rent_ratio(property_obj.price, annual_rent)

        # Paris typically has 20-25 years price-to-rent ratio
        assert 15 <= ptr <= 30

    def test_all_cash_purchase_scenario(self, sample_property_data):
        """Test scenario with all-cash purchase (no mortgage)"""
        property_obj = Property(**sample_property_data)

        # All cash purchase - no mortgage
        monthly_rent = 2000
        annual_operating_expenses = 6000

        gmi = financial.gross_monthly_income(monthly_rent)
        vcl = financial.vacancy_credit_loss(gmi, 0.05)
        noi = financial.noi_calculation(gmi, vcl, annual_operating_expenses)

        # With no debt, DSCR should be infinity (no ADS)
        ads = financial.annual_debt_service(0)  # No mortgage payment
        dscr = financial.dscr_calculation(noi, ads)

        assert dscr == float('inf')

        # Cap rate calculation
        cap_rate = financial.cap_rate(noi, property_obj.price)
        assert cap_rate > 0

        # Cash-on-cash return equals cap rate in all-cash scenario (before tax)
        coc = financial.cash_on_cash(noi, property_obj.price)
        assert coc == pytest.approx(cap_rate, rel=0.001)