"""
Unit tests for backend/models/property.py
"""

import pytest
from pydantic import ValidationError
from backend.models.property import Address, Property, Listing


class TestAddress:
    """Tests for Address model"""

    def test_valid_address(self):
        """Test creating valid address."""
        address = Address(
            street="10 Rue de Rivoli",
            city="Paris",
            postal_code="75001",
            quartier="Louvre"
        )
        assert address.street == "10 Rue de Rivoli"
        assert address.city == "Paris"
        assert address.postal_code == "75001"
        assert address.quartier == "Louvre"

    def test_default_city(self):
        """Test default city is Paris."""
        address = Address(
            street="10 Rue de Rivoli",
            postal_code="75001"
        )
        assert address.city == "Paris"

    def test_invalid_postal_code(self):
        """Test invalid postal code format."""
        with pytest.raises(ValidationError):
            Address(
                street="10 Rue de Rivoli",
                postal_code="7500"  # Too short
            )

    def test_invalid_postal_code_letters(self):
        """Test postal code with letters."""
        with pytest.raises(ValidationError):
            Address(
                street="10 Rue de Rivoli",
                postal_code="ABCDE"
            )


class TestProperty:
    """Tests for Property model"""

    def test_valid_property(self, sample_property_data):
        """Test creating valid property."""
        property_obj = Property(**sample_property_data)
        assert property_obj.price == 500000
        assert property_obj.surface == 50
        assert property_obj.rooms == 2

    def test_price_per_m2_calculation(self, sample_property_data):
        """Test price_per_m2 is calculated correctly."""
        property_obj = Property(**sample_property_data)
        assert property_obj.price_per_m2 == pytest.approx(10000, rel=0.01)

    def test_negative_price(self, sample_property_data):
        """Test that negative price is rejected."""
        sample_property_data['price'] = -100000
        with pytest.raises(ValidationError):
            Property(**sample_property_data)

    def test_zero_surface(self, sample_property_data):
        """Test that zero surface is rejected."""
        sample_property_data['surface'] = 0
        with pytest.raises(ValidationError):
            Property(**sample_property_data)

    def test_invalid_dpe(self, sample_property_data):
        """Test invalid DPE grade."""
        sample_property_data['dpe'] = "H"  # Invalid grade
        with pytest.raises(ValidationError):
            Property(**sample_property_data)

    def test_valid_dpe_grades(self, sample_property_data):
        """Test all valid DPE grades."""
        valid_grades = ["A", "B", "C", "D", "E", "F", "G"]
        for grade in valid_grades:
            sample_property_data['dpe'] = grade
            property_obj = Property(**sample_property_data)
            assert property_obj.dpe == grade


class TestListing:
    """Tests for Listing model"""

    def test_valid_listing(self, sample_property_data):
        """Test creating valid listing."""
        listing = Listing(
            **sample_property_data,
            url="https://example.com/listing",
            source="seloger",
            listing_date="2024-01-15"
        )
        assert listing.url == "https://example.com/listing"
        assert listing.source == "seloger"
        assert listing.listing_date == "2024-01-15"

    def test_optional_fields(self, sample_property_data):
        """Test listing with optional fields."""
        listing = Listing(
            **sample_property_data,
            url="https://example.com/listing"
        )
        assert listing.source is None
        assert listing.listing_date is None