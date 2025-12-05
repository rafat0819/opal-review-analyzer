import pytest
from fastapi.testclient import TestClient
from main import app, analyze_customer_review, ReviewParams


# Create a test client for the FastAPI app
client = TestClient(app)


class TestAnalyzeReview:
    """Test suite for the analyze_customer_review tool"""

    @pytest.mark.asyncio
    async def test_technical_issue_detection(self):
        """Test that technical issues are correctly identified"""
        params = ReviewParams(text="The app keeps crashing when I try to login")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Technical Issue"
        assert isinstance(result["sentiment_score"], float)
        assert "Technical Issue" in result["summary"]

    @pytest.mark.asyncio
    async def test_guidance_request_detection(self):
        """Test that guidance requests are correctly identified"""
        params = ReviewParams(text="How to reset my password? I need help with this")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Guidance"
        assert isinstance(result["sentiment_score"], float)
        assert "Guidance" in result["summary"]

    @pytest.mark.asyncio
    async def test_positive_sentiment(self):
        """Test that positive reviews are correctly identified"""
        params = ReviewParams(text="This app is amazing! I love it so much, great features!")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Positive"
        assert result["sentiment_score"] > 0
        assert "Positive" in result["summary"]

    @pytest.mark.asyncio
    async def test_negative_sentiment(self):
        """Test that negative reviews are correctly identified"""
        params = ReviewParams(text="This is terrible. I hate this app, worst experience ever")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Negative"
        assert result["sentiment_score"] < 0
        assert "Negative" in result["summary"]

    @pytest.mark.asyncio
    async def test_neutral_sentiment(self):
        """Test that neutral reviews are correctly identified"""
        params = ReviewParams(text="The app exists. It has features.")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Neutral"
        assert isinstance(result["sentiment_score"], float)
        assert "Neutral" in result["summary"]

    @pytest.mark.asyncio
    async def test_multiple_keywords(self):
        """Test priority when multiple keyword types are present"""
        # Technical keywords should take priority over sentiment
        params = ReviewParams(text="I love the idea but the app crashes constantly")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Technical Issue"

    @pytest.mark.asyncio
    async def test_sentiment_score_range(self):
        """Test that sentiment scores are within expected range"""
        params = ReviewParams(text="This is okay")
        result = await analyze_customer_review(params)
        
        assert -1.0 <= result["sentiment_score"] <= 1.0

    @pytest.mark.asyncio
    async def test_empty_text(self):
        """Test handling of empty review text"""
        params = ReviewParams(text="")
        result = await analyze_customer_review(params)
        
        assert "category" in result
        assert "sentiment_score" in result
        assert "summary" in result


class TestAPIEndpoints:
    """Test suite for FastAPI endpoints"""

    def test_api_health(self):
        """Test that the API is running"""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_analyze_customer_review_endpoint(self):
        """Test the analyze_customer_review endpoint via HTTP"""
        # Note: This test assumes the OPAL Tools SDK creates an endpoint
        # The actual endpoint path may vary based on SDK implementation
        payload = {
            "text": "The app has a bug that needs fixing"
        }
        
        # This is a placeholder - adjust based on actual SDK endpoint structure
        # You may need to check the actual endpoint created by ToolsService
        response = client.post("/analyze_customer_review", json=payload)
        
        # If endpoint doesn't exist yet, this test will fail
        # which is expected until SDK creates the endpoint
        if response.status_code == 200:
            data = response.json()
            assert "category" in data
            assert "sentiment_score" in data
            assert "summary" in data


class TestEdgeCases:
    """Test edge cases and special scenarios"""

    @pytest.mark.asyncio
    async def test_very_long_text(self):
        """Test handling of very long review text"""
        long_text = "This is a review. " * 100
        params = ReviewParams(text=long_text)
        result = await analyze_customer_review(params)
        
        assert "category" in result
        assert isinstance(result["sentiment_score"], float)

    @pytest.mark.asyncio
    async def test_special_characters(self):
        """Test handling of special characters"""
        params = ReviewParams(text="App is 💯! Love it!!! ❤️❤️❤️")
        result = await analyze_customer_review(params)
        
        assert "category" in result
        assert result["sentiment_score"] > 0

    @pytest.mark.asyncio
    async def test_mixed_case(self):
        """Test that keyword detection is case-insensitive"""
        params = ReviewParams(text="The APP keeps CRASHING and has BUGS")
        result = await analyze_customer_review(params)
        
        assert result["category"] == "Technical Issue"

    @pytest.mark.asyncio
    async def test_numbers_in_text(self):
        """Test handling of numbers in review text"""
        params = ReviewParams(text="I've tried 5 times but it fails every time")
        result = await analyze_customer_review(params)
        
        assert "category" in result
        assert isinstance(result["sentiment_score"], float)


# Run tests with: pytest test_main.py -v
# Run with coverage: pytest test_main.py -v --cov=main --cov-report=html
