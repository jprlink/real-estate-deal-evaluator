"""
Pytest configuration and shared fixtures.
"""

import pytest
from typing import Dict, Any


@pytest.fixture
def sample_property_data() -> Dict[str, Any]:
    """Sample property data for testing."""
    return {
        "address": {
            "street": "10 Rue de Rivoli",
            "city": "Paris",
            "postal_code": "75001",
            "quartier": "Louvre"
        },
        "price": 500000,
        "surface": 50,
        "rooms": 2,
        "bedrooms": 1,
        "floor": 3,
        "dpe": "D",
        "ges": "D"
    }


@pytest.fixture
def sample_financial_inputs() -> Dict[str, Any]:
    """Sample financial inputs for testing."""
    return {
        "down_payment": 100000,
        "loan_amount": 400000,
        "annual_interest_rate": 0.03,
        "loan_term_years": 20,
        "monthly_rent": 2000,
        "annual_operating_expenses": 6000,
        "vacancy_rate": 0.05,
        "annual_appreciation": 0.02,
        "hold_period_years": 10,
        "marginal_tax_rate": 0.30
    }


@pytest.fixture
def sample_cash_flows() -> list:
    """Sample cash flows for IRR/NPV testing."""
    return [
        -100000,  # Initial investment
        15000,    # Year 1
        15000,    # Year 2
        15000,    # Year 3
        15000,    # Year 4
        15000,    # Year 5
        15000,    # Year 6
        15000,    # Year 7
        15000,    # Year 8
        15000,    # Year 9
        165000    # Year 10 (cash flow + sale proceeds)
    ]


@pytest.fixture
def mock_brave_search_results() -> list:
    """Mock Brave Search API results."""
    return [
        {
            "title": "Appartement 2 pièces 50m² Paris 1er - 500,000€",
            "url": "https://example.com/listing1",
            "description": "Bel appartement 2 pièces de 50m² au 3ème étage",
            "published_date": "2024-01-15"
        },
        {
            "title": "Paris 75001 - 2P 48m² - 480,000€",
            "url": "https://example.com/listing2",
            "description": "Appartement rénové proche Louvre",
            "published_date": "2024-01-10"
        }
    ]


@pytest.fixture
def mock_dvf_comps() -> list:
    """Mock DVF comparable sales."""
    return [
        {
            "date": "2024-12-01",
            "price": 495000,
            "surface": 51,
            "price_per_m2": 9706,
            "address": "12 Rue de Rivoli",
            "rooms": 2
        },
        {
            "date": "2024-11-15",
            "price": 510000,
            "surface": 52,
            "price_per_m2": 9808,
            "address": "8 Rue Saint-Honoré",
            "rooms": 2
        }
    ]


@pytest.fixture
def mock_rent_cap_data() -> Dict[str, Any]:
    """Mock Paris rent control data."""
    return {
        "quartier": "Louvre",
        "rooms": 2,
        "furnished": False,
        "reference_rent_eur_m2": 28.0,
        "ceiling_rent_eur_m2": 33.6,
        "construction_year_adjustment": 0.0
    }