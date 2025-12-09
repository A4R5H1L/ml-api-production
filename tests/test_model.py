"""
Tests for the image classifier model.

This module contains unit tests for the ImageClassifier class,
testing model initialization, preprocessing, and prediction functionality.
"""

import pytest
from PIL import Image
import numpy as np
import torch

from app.models.classifier import ImageClassifier, get_classifier


@pytest.fixture
def sample_image():
    """Create a sample RGB image for testing."""
    # Create a 224x224 RGB image with random data
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    return Image.fromarray(img_array)


@pytest.fixture
def grayscale_image():
    """Create a sample grayscale image for testing."""
    img_array = np.random.randint(0, 255, (224, 224), dtype=np.uint8)
    return Image.fromarray(img_array, mode='L')


class TestImageClassifier:
    """Test cases for ImageClassifier class."""
    
    def test_classifier_initialization(self):
        """Test that classifier initializes correctly."""
        classifier = ImageClassifier()
        
        assert classifier.model is None  # Model should be lazy-loaded
        assert classifier.device in ['cpu', 'cuda']
        assert classifier.transform is not None
        assert len(classifier.class_labels) == 1000
    
    def test_classifier_device_selection_cpu(self):
        """Test that classifier can be initialized with CPU device."""
        classifier = ImageClassifier(device='cpu')
        assert classifier.device == 'cpu'
    
    def test_preprocess_rgb_image(self, sample_image):
        """Test preprocessing of RGB images."""
        classifier = ImageClassifier()
        tensor = classifier.preprocess_image(sample_image)
        
        # Check tensor shape: [batch_size, channels, height, width]
        assert tensor.shape == (1, 3, 224, 224)
        assert isinstance(tensor, torch.Tensor)
    
    def test_preprocess_grayscale_image(self, grayscale_image):
        """Test preprocessing converts grayscale to RGB."""
        classifier = ImageClassifier()
        tensor = classifier.preprocess_image(grayscale_image)
        
        # Should be converted to RGB
        assert tensor.shape == (1, 3, 224, 224)
    
    def test_predict_returns_top_k(self, sample_image):
        """Test that predict returns correct number of predictions."""
        classifier = ImageClassifier()
        predictions = classifier.predict(sample_image, top_k=5)
        
        assert len(predictions) == 5
        assert all(isinstance(pred, tuple) for pred in predictions)
        assert all(len(pred) == 2 for pred in predictions)
    
    def test_predict_probabilities_sum_to_one(self, sample_image):
        """Test that prediction probabilities are valid."""
        classifier = ImageClassifier()
        predictions = classifier.predict(sample_image, top_k=5)
        
        # All probabilities should be between 0 and 1
        for class_name, prob in predictions:
            assert 0 <= prob <= 1
            assert isinstance(class_name, str)
    
    def test_predict_sorted_by_confidence(self, sample_image):
        """Test that predictions are sorted by confidence in descending order."""
        classifier = ImageClassifier()
        predictions = classifier.predict(sample_image, top_k=5)
        
        probabilities = [prob for _, prob in predictions]
        # Check that probabilities are in descending order
        assert probabilities == sorted(probabilities, reverse=True)
    
    def test_model_lazy_loading(self):
        """Test that model is loaded only when needed."""
        classifier = ImageClassifier()
        assert classifier.model is None
        
        # Create a sample image and predict
        sample_img = Image.new('RGB', (224, 224))
        classifier.predict(sample_img)
        
        # Model should now be loaded
        assert classifier.model is not None
    
    def test_get_classifier_singleton(self):
        """Test that get_classifier returns the same instance."""
        classifier1 = get_classifier()
        classifier2 = get_classifier()
        
        assert classifier1 is classifier2


class TestClassifierEdgeCases:
    """Test edge cases and error handling."""
    
    def test_predict_with_different_top_k(self, sample_image):
        """Test prediction with different top_k values."""
        classifier = ImageClassifier()
        
        predictions_3 = classifier.predict(sample_image, top_k=3)
        predictions_10 = classifier.predict(sample_image, top_k=10)
        
        assert len(predictions_3) == 3
        assert len(predictions_10) == 10
    
    def test_predict_with_small_image(self):
        """Test that small images are properly resized."""
        classifier = ImageClassifier()
        small_image = Image.new('RGB', (50, 50))
        
        predictions = classifier.predict(small_image, top_k=3)
        assert len(predictions) == 3
    
    def test_predict_with_large_image(self):
        """Test that large images are properly resized."""
        classifier = ImageClassifier()
        large_image = Image.new('RGB', (1000, 1000))
        
        predictions = classifier.predict(large_image, top_k=3)
        assert len(predictions) == 3
