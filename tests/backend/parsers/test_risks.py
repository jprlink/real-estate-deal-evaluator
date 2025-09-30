"""
Unit tests for backend/parsers/risks.py
"""

import pytest
from backend.parsers import risks


class TestParseGeorisquesHTML:
    """Tests for parse_georisques_html()"""

    def test_parse_flood_risk(self):
        """Test flood risk extraction."""
        html = """
        <div class="risks">
            <p>Risque d'inondation: Niveau moyen</p>
        </div>
        """
        result = risks.parse_georisques_html(html)

        assert len(result["natural_risks"]) > 0
        flood_risk = next((r for r in result["natural_risks"] if r["type"] == "flood"), None)
        assert flood_risk is not None
        assert flood_risk["level"] == "medium"

    def test_parse_seismic_zone(self):
        """Test seismic zone extraction."""
        html = "<p>Zone sismique: 3</p>"
        result = risks.parse_georisques_html(html)

        assert result["seismic_zone"] == 3

    def test_parse_radon_potential(self):
        """Test radon potential extraction."""
        html = "<p>Potentiel radon: 2</p>"
        result = risks.parse_georisques_html(html)

        assert result["radon_potential"] == 2

    def test_parse_technological_risks(self):
        """Test technological risk extraction."""
        html = """
        <div>
            <p>Site ICPE à 150 mètres</p>
            <p>Installation SEVESO</p>
        </div>
        """
        result = risks.parse_georisques_html(html)

        assert len(result["technological_risks"]) >= 2
        icpe = next((r for r in result["technological_risks"] if r["type"] == "industrial_classified"), None)
        assert icpe is not None
        assert icpe["distance_meters"] == 150

    def test_parse_soil_pollution(self):
        """Test soil pollution detection."""
        html = "<p>Site pollué identifié</p>"
        result = risks.parse_georisques_html(html)

        assert result["soil_pollution"] is True

    def test_parse_complete_report(self):
        """Test parsing complete Géorisques report."""
        html = """
        <html>
            <body>
                <h1>Rapport Géorisques</h1>
                <section>
                    <h2>Risques naturels</h2>
                    <p>Inondation: Niveau faible</p>
                    <p>Mouvement de terrain: Niveau fort</p>
                </section>
                <section>
                    <h2>Zone sismique</h2>
                    <p>Zone sismique: 2</p>
                </section>
                <section>
                    <h2>Potentiel radon</h2>
                    <p>Potentiel radon: 1</p>
                </section>
                <section>
                    <h2>Risques technologiques</h2>
                    <p>ICPE à 500 mètres</p>
                </section>
            </body>
        </html>
        """
        result = risks.parse_georisques_html(html)

        # Should have natural risks
        assert len(result["natural_risks"]) >= 2

        # Should have seismic and radon data
        assert result["seismic_zone"] == 2
        assert result["radon_potential"] == 1

        # Should have technological risks
        assert len(result["technological_risks"]) >= 1

        # Should have overall risk level
        assert result["overall_risk_level"] in ["low", "medium", "high"]

        # Should have summary
        assert len(result["summary"]) > 0

    def test_parse_empty_html(self):
        """Test parsing empty HTML."""
        result = risks.parse_georisques_html("")

        assert len(result["natural_risks"]) == 0
        assert len(result["technological_risks"]) == 0
        assert result["overall_risk_level"] == "low"  # No risks = low


class TestCalculateOverallRiskLevel:
    """Tests for _calculate_overall_risk_level()"""

    def test_low_risk_scenario(self):
        """Test low risk calculation."""
        risk_data = {
            "natural_risks": [{"level": "low"}],
            "seismic_zone": 1,
            "radon_potential": 1,
            "technological_risks": [],
            "soil_pollution": False
        }
        level = risks._calculate_overall_risk_level(risk_data)
        assert level == "low"

    def test_high_risk_scenario(self):
        """Test high risk calculation."""
        risk_data = {
            "natural_risks": [
                {"level": "high"},
                {"level": "high"}
            ],
            "seismic_zone": 4,
            "radon_potential": 3,
            "technological_risks": [
                {"distance_meters": 50}
            ],
            "soil_pollution": True
        }
        level = risks._calculate_overall_risk_level(risk_data)
        assert level == "high"

    def test_medium_risk_scenario(self):
        """Test medium risk calculation."""
        risk_data = {
            "natural_risks": [{"level": "medium"}],
            "seismic_zone": 2,
            "radon_potential": 2,
            "technological_risks": [{"distance_meters": 300}],
            "soil_pollution": False
        }
        level = risks._calculate_overall_risk_level(risk_data)
        assert level == "medium"


class TestExtractCrimeData:
    """Tests for extract_crime_data()"""

    def test_parse_crime_categories(self):
        """Test crime category extraction."""
        html = """
        <div class="statistics">
            <p>Vol: 45</p>
            <p>Cambriolage: 12</p>
            <p>Agression: 8</p>
        </div>
        """
        result = risks.extract_crime_data(html, "Le Marais")

        assert "theft" in result["categories"]
        assert "burglary" in result["categories"]
        assert "assault" in result["categories"]

    def test_parse_comparison(self):
        """Test national comparison extraction."""
        html = "<p>Crime rate is above average for the region</p>"
        result = risks.extract_crime_data(html, "Test")

        assert result["national_comparison"] == "above_average"

    def test_parse_trend(self):
        """Test trend extraction."""
        html = "<p>Crime is decreasing in this area</p>"
        result = risks.extract_crime_data(html, "Test")

        assert result["trend"] == "decreasing"

    def test_default_values(self):
        """Test default values with no data."""
        result = risks.extract_crime_data("", "Test")

        assert result["quartier"] == "Test"
        assert result["crime_score"] == 50  # Default median
        assert result["national_comparison"] == "average"
        assert result["trend"] == "stable"