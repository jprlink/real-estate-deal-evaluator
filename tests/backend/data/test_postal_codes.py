"""
Unit tests for postal code database.
"""

import pytest
from backend.data.postal_codes import (
    get_city_from_postal_code,
    get_department_from_postal_code,
    get_city_and_department
)


def test_get_city_paris():
    """Test getting city name for Paris postal codes."""
    assert get_city_from_postal_code("75001") == "Paris"
    assert get_city_from_postal_code("75010") == "Paris"
    assert get_city_from_postal_code("75020") == "Paris"


def test_get_city_hauts_de_seine():
    """Test getting city names for Hauts-de-Seine (92)."""
    assert get_city_from_postal_code("92000") == "Nanterre"
    assert get_city_from_postal_code("92100") == "Boulogne-Billancourt"
    assert get_city_from_postal_code("92200") == "Neuilly-sur-Seine"


def test_get_city_seine_saint_denis():
    """Test getting city names for Seine-Saint-Denis (93)."""
    assert get_city_from_postal_code("93000") == "Bobigny"
    assert get_city_from_postal_code("93100") == "Montreuil"
    assert get_city_from_postal_code("93200") == "Saint-Denis"


def test_get_city_major_cities():
    """Test getting city names for major French cities."""
    assert get_city_from_postal_code("69001") == "Lyon"
    assert get_city_from_postal_code("13001") == "Marseille"
    assert get_city_from_postal_code("31000") == "Toulouse"
    assert get_city_from_postal_code("33000") == "Bordeaux"


def test_get_city_invalid():
    """Test getting city for invalid postal codes."""
    assert get_city_from_postal_code("99999") is None
    assert get_city_from_postal_code("1234") is None  # Too short
    assert get_city_from_postal_code("") is None
    assert get_city_from_postal_code(None) is None


def test_get_department():
    """Test getting department codes."""
    assert get_department_from_postal_code("75001") == "75"
    assert get_department_from_postal_code("92000") == "92"
    assert get_department_from_postal_code("69001") == "69"


def test_get_department_fallback():
    """Test department extraction fallback for unknown postal codes."""
    # Should still extract first 2 digits
    assert get_department_from_postal_code("99999") == "99"
    assert get_department_from_postal_code("01234") == "01"


def test_get_city_and_department():
    """Test getting both city and department."""
    city, dept = get_city_and_department("75001")
    assert city == "Paris"
    assert dept == "75"

    city, dept = get_city_and_department("92100")
    assert city == "Boulogne-Billancourt"
    assert dept == "92"


def test_get_city_and_department_unknown():
    """Test getting city and department for unknown postal code."""
    city, dept = get_city_and_department("99999")
    assert city is None
    assert dept == "99"  # Fallback to extracted department
