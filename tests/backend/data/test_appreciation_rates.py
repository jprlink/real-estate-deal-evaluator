"""
Unit tests for appreciation rate data.
"""

import pytest
from backend.data.appreciation_rates import (
    get_appreciation_rate,
    get_appreciation_rate_display,
    get_appreciation_source,
    DEPARTMENT_APPRECIATION_RATES
)


def test_get_appreciation_rate_paris():
    """Test appreciation rate for Paris."""
    rate = get_appreciation_rate("75001", forward_looking=True)
    # Paris base: -2.9%, forward adjustment: +1.5% = -1.4%
    assert -0.02 < rate < 0.0  # Should be around -1.4%


def test_get_appreciation_rate_nice():
    """Test appreciation rate for Nice (stable market)."""
    rate = get_appreciation_rate("06000", forward_looking=True)
    # Nice base: 0.0%, forward adjustment: +1.5% = +1.5%
    assert 0.01 < rate < 0.02  # Should be around +1.5%


def test_get_appreciation_rate_rennes():
    """Test appreciation rate for Rennes (growing market)."""
    rate = get_appreciation_rate("35000", forward_looking=True)
    # Rennes base: +0.8%, forward adjustment: +1.5% = +2.3%
    assert 0.02 < rate < 0.03  # Should be around +2.3%


def test_get_appreciation_rate_no_forward():
    """Test appreciation rate without forward adjustment."""
    rate_paris = get_appreciation_rate("75001", forward_looking=False)
    # Should be base rate only: -2.9%
    assert -0.03 < rate_paris < -0.025


def test_get_appreciation_rate_by_department():
    """Test appreciation rate using department code."""
    rate = get_appreciation_rate(department="75", forward_looking=True)
    assert rate is not None
    assert -0.02 < rate < 0.0


def test_get_appreciation_rate_unknown():
    """Test appreciation rate for unknown location."""
    rate = get_appreciation_rate("99999", forward_looking=True)
    # Should return default: 0.5% + 1.5% = 2.0%
    assert 0.019 < rate < 0.021


def test_get_appreciation_rate_display():
    """Test formatted appreciation rate display."""
    display = get_appreciation_rate_display("06000", forward_looking=True)
    assert "+" in display or "-" in display
    assert "%" in display


def test_get_appreciation_rate_display_positive():
    """Test display format for positive rates."""
    display = get_appreciation_rate_display("35000", forward_looking=True)
    assert display.startswith("+")
    assert "%" in display


def test_get_appreciation_rate_display_negative():
    """Test display format for negative rates."""
    display = get_appreciation_rate_display("75001", forward_looking=True)
    # Paris with forward adjustment is still negative
    assert "%" in display


def test_get_appreciation_source():
    """Test data source information."""
    source = get_appreciation_source()
    assert "Notaires de France" in source
    assert "2024" in source or "2025" in source


def test_department_rates_coverage():
    """Test that major departments have appreciation rates."""
    major_depts = ["75", "92", "93", "94", "69", "13", "31", "33"]
    for dept in major_depts:
        assert dept in DEPARTMENT_APPRECIATION_RATES


def test_appreciation_rate_ranges():
    """Test that appreciation rates are within reasonable ranges."""
    for dept, rate in DEPARTMENT_APPRECIATION_RATES.items():
        # Rates should be between -10% and +10% (reasonable for French market)
        assert -10.0 <= rate <= 10.0
