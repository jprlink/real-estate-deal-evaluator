"""
Unit tests for backend/parsers/listing.py
"""

import pytest
from backend.parsers import listing


class TestParseListingHTML:
    """Tests for parse_listing_html()"""

    def test_parse_price(self):
        """Test price extraction from HTML."""
        html = """
        <div class="listing">
            <span class="price">500 000 €</span>
        </div>
        """
        result = listing.parse_listing_html(html)
        assert result["price"] == 500000

    def test_parse_surface(self):
        """Test surface area extraction."""
        html = "<p>Surface: 50 m²</p>"
        result = listing.parse_listing_html(html)
        assert result["surface"] == 50

    def test_parse_rooms(self):
        """Test room count extraction."""
        html = "<div>2 pièces</div>"
        result = listing.parse_listing_html(html)
        assert result["rooms"] == 2

    def test_parse_dpe(self):
        """Test DPE grade extraction."""
        html = "<span>DPE: D</span>"
        result = listing.parse_listing_html(html)
        assert result["dpe"] == "D"

    def test_parse_postal_code(self):
        """Test postal code extraction."""
        html = "<p>Located in 75003 Paris</p>"
        result = listing.parse_listing_html(html)
        assert result["address"]["postal_code"] == "75003"
        assert result["address"]["city"] == "Paris"

    def test_parse_complete_listing(self):
        """Test parsing complete listing HTML."""
        html = """
        <div class="listing">
            <h1>Appartement 2 pièces 50m²</h1>
            <span class="price">350 000 €</span>
            <p>Surface: 50 m²</p>
            <p>2 pièces, 1 chambre</p>
            <p>3ème étage avec ascenseur</p>
            <p>DPE: D</p>
            <p>Adresse: 10 Rue de Rivoli, 75001 Paris</p>
            <ul>
                <li>Balcon</li>
                <li>Parking</li>
            </ul>
        </div>
        """
        result = listing.parse_listing_html(html)

        assert result["price"] == 350000
        assert result["surface"] == 50
        assert result["rooms"] == 2
        assert result["bedrooms"] == 1
        assert result["floor"] == 3
        assert result["dpe"] == "D"
        assert result["address"]["postal_code"] == "75001"
        assert "balcon" in result["features"]

    def test_parse_empty_html(self):
        """Test parsing empty HTML."""
        result = listing.parse_listing_html("")
        assert result["price"] is None
        assert result["surface"] is None
        assert result["rooms"] is None


class TestNormalizeListingData:
    """Tests for normalize_listing_data()"""

    def test_normalize_complete_data(self):
        """Test normalization with complete data."""
        raw_data = {
            "address": {"street": "10 Rue de Rivoli", "postal_code": "75001"},
            "price": 500000,
            "surface": 50,
            "rooms": 2,
            "bedrooms": 1
        }
        result = listing.normalize_listing_data(raw_data)

        assert result["address"]["city"] == "Paris"
        assert result["bedrooms"] == 1

    def test_estimate_bedrooms(self):
        """Test bedroom estimation when not provided."""
        raw_data = {
            "address": {},
            "rooms": 3,
            "bedrooms": None
        }
        result = listing.normalize_listing_data(raw_data)

        # Should estimate 2 bedrooms for 3-room apartment
        assert result["bedrooms"] == 2

    def test_remove_none_values(self):
        """Test removal of None values from address."""
        raw_data = {
            "address": {"street": None, "postal_code": "75001"},
            "price": 500000
        }
        result = listing.normalize_listing_data(raw_data)

        assert "street" not in result["address"]
        assert "postal_code" in result["address"]


class TestExtractListingURLInfo:
    """Tests for extract_listing_url_info()"""

    def test_seloger_url(self):
        """Test SeLoger URL parsing."""
        url = "https://www.seloger.com/annonces/achat/123456"
        result = listing.extract_listing_url_info(url)

        assert result["source"] == "seloger"
        assert result["listing_id"] == "123456"
        assert result["url"] == url

    def test_leboncoin_url(self):
        """Test LeBonCoin URL parsing."""
        url = "https://www.leboncoin.fr/ventes_immobilieres/789012"
        result = listing.extract_listing_url_info(url)

        assert result["source"] == "leboncoin"
        assert result["listing_id"] == "789012"

    def test_unknown_site(self):
        """Test URL from unknown site."""
        url = "https://www.unknown-site.com/listing/456789"
        result = listing.extract_listing_url_info(url)

        assert result["source"] is None
        assert result["listing_id"] == "456789"