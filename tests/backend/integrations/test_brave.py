"""
Unit tests for backend/integrations/brave.py
"""

import pytest
from unittest.mock import AsyncMock, patch
from backend.integrations import brave


class TestSearchWeb:
    """Tests for search_web()"""

    @pytest.mark.asyncio
    async def test_successful_search(self):
        """Test successful Brave Search API call."""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "web": {
                "results": [
                    {
                        "title": "Test Result 1",
                        "url": "https://example.com/1",
                        "description": "Test description 1",
                        "age": "2024-01-15"
                    },
                    {
                        "title": "Test Result 2",
                        "url": "https://example.com/2",
                        "description": "Test description 2",
                        "age": "2024-01-10"
                    }
                ]
            }
        }

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            results = await brave.search_web(
                api_key="test_key",
                query="test query",
                count=10
            )

            assert len(results) == 2
            assert results[0]['title'] == "Test Result 1"
            assert results[0]['url'] == "https://example.com/1"
            assert results[1]['title'] == "Test Result 2"

    @pytest.mark.asyncio
    async def test_rate_limit_error(self):
        """Test handling of rate limit (429) error."""
        mock_response = AsyncMock()
        mock_response.status_code = 429

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            with pytest.raises(Exception, match="Rate limit exceeded"):
                await brave.search_web(
                    api_key="test_key",
                    query="test query"
                )

    @pytest.mark.asyncio
    async def test_empty_results(self):
        """Test handling of empty search results."""
        mock_response = AsyncMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"web": {"results": []}}

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            results = await brave.search_web(
                api_key="test_key",
                query="nonexistent query"
            )

            assert results == []

    @pytest.mark.asyncio
    async def test_http_error(self):
        """Test handling of HTTP errors."""
        mock_response = AsyncMock()
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Server error")

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            with pytest.raises(Exception):
                await brave.search_web(
                    api_key="test_key",
                    query="test query"
                )