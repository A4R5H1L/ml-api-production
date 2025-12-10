"""
Tests for API endpoints.

This module contains integration tests for all API endpoints,
including health checks and prediction functionality.
"""

import io

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_endpoint_returns_200(self):
        """Test that health endpoint returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_response_structure(self):
        """Test that health endpoint returns correct structure."""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "version" in data
        assert "model_loaded" in data
        assert data["status"] == "healthy"

    def test_health_endpoint_includes_version(self):
        """Test that health endpoint includes API version."""
        response = client.get("/health")
        data = response.json()

        assert data["version"] == "0.1.0"


class TestRootEndpoint:
    """Tests for root endpoint."""

    def test_root_endpoint_returns_200(self):
        """Test that root endpoint returns 200 OK."""
        response = client.get("/")
        assert response.status_code == 200

    def test_root_endpoint_includes_api_info(self):
        """Test that root endpoint includes API information."""
        response = client.get("/")
        data = response.json()

        assert "name" in data
        assert "version" in data
        assert "docs" in data
        assert "health" in data


class TestPredictionEndpoint:
    """Tests for prediction endpoint."""

    @pytest.fixture
    def sample_image_bytes(self):
        """Create a sample image as bytes for upload."""
        # Create a simple RGB image
        img = Image.new("RGB", (224, 224), color=(73, 109, 137))
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="JPEG")
        img_bytes.seek(0)
        return img_bytes

    def test_predict_endpoint_with_valid_image(self, sample_image_bytes):
        """Test prediction with a valid image."""
        files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
        response = client.post("/predict", files=files)

        assert response.status_code == 200
        data = response.json()

        assert data["success"] is True
        assert "predictions" in data
        assert len(data["predictions"]) == 5  # Default top_k

    def test_predict_endpoint_response_structure(self, sample_image_bytes):
        """Test that prediction response has correct structure."""
        files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
        response = client.post("/predict", files=files)

        data = response.json()
        predictions = data["predictions"]

        # Check each prediction has class_name and confidence
        for pred in predictions:
            assert "class_name" in pred
            assert "confidence" in pred
            assert isinstance(pred["class_name"], str)
            assert isinstance(pred["confidence"], float)
            assert 0 <= pred["confidence"] <= 1

    def test_predict_endpoint_with_custom_top_k(self, sample_image_bytes):
        """Test prediction with custom top_k parameter."""
        files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
        response = client.post("/predict?top_k=3", files=files)

        assert response.status_code == 200
        data = response.json()

        assert len(data["predictions"]) == 3

    def test_predict_endpoint_without_file(self):
        """Test that prediction requires a file."""
        response = client.post("/predict")
        assert response.status_code == 422  # Validation error

    def test_predict_endpoint_with_invalid_file_type(self):
        """Test prediction with non-image file."""
        files = {"file": ("test.txt", io.BytesIO(b"not an image"), "text/plain")}
        response = client.post("/predict", files=files)

        assert response.status_code == 400

    def test_predict_endpoint_with_invalid_top_k(self, sample_image_bytes):
        """Test prediction with invalid top_k value."""
        files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}

        # Test with top_k too large
        response = client.post("/predict?top_k=20", files=files)
        assert response.status_code == 400

        # Test with top_k too small
        response = client.post("/predict?top_k=0", files=files)
        assert response.status_code == 400

    def test_predictions_sorted_by_confidence(self, sample_image_bytes):
        """Test that predictions are sorted by confidence."""
        files = {"file": ("test.jpg", sample_image_bytes, "image/jpeg")}
        response = client.post("/predict", files=files)

        data = response.json()
        predictions = data["predictions"]

        # Check that confidences are in descending order
        confidences = [pred["confidence"] for pred in predictions]
        assert confidences == sorted(confidences, reverse=True)


class TestAPIDocumentation:
    """Tests for API documentation endpoints."""

    def test_openapi_schema_available(self):
        """Test that OpenAPI schema is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_swagger_docs_available(self):
        """Test that Swagger UI is available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_available(self):
        """Test that ReDoc documentation is available."""
        response = client.get("/redoc")
        assert response.status_code == 200
