"""
Image classifier using pre-trained ResNet-18 model.

This module provides a wrapper around PyTorch's ResNet-18 model for image classification.
The model is loaded lazily on first prediction to optimize startup time.
"""

from typing import List, Tuple, Optional
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import json
import logging

logger = logging.getLogger(__name__)


class ImageClassifier:
    """
    Image classification using pre-trained ResNet-18 model.
    
    This class provides a simple interface for image classification using
    a pre-trained ResNet-18 model. The model is loaded lazily on first use
    and cached for subsequent predictions.
    
    Attributes:
        model: The loaded PyTorch model (loaded on first prediction)
        device: The device to run inference on (CPU or CUDA)
        transform: Image preprocessing pipeline
        class_labels: List of ImageNet class labels
    """
    
    def __init__(self, device: Optional[str] = None):
        """
        Initialize the image classifier.
        
        Args:
            device: Device to run inference on ('cuda' or 'cpu').
                   If None, automatically selects CUDA if available.
        """
        self.model = None
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Classifier initialized with device: {self.device}")
        
        # Image preprocessing pipeline for ResNet
        # ImageNet normalization values
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Load ImageNet class labels
        self.class_labels = self._load_imagenet_labels()
    
    def _load_imagenet_labels(self) -> List[str]:
        """
        Load ImageNet class labels.
        
        Returns:
            List of 1000 ImageNet class labels
        """
        # Simple class labels for ImageNet (1000 classes)
        # In production, you'd load this from a file
        # For now, returning generic labels
        return [f"class_{i}" for i in range(1000)]
    
    def _load_model(self):
        """
        Load the pre-trained ResNet-18 model.
        
        This method is called lazily on first prediction to optimize
        startup time. The model is loaded only when needed.
        """
        if self.model is None:
            logger.info("Loading ResNet-18 model...")
            # Load pre-trained ResNet-18
            self.model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            logger.info("Model loaded successfully")
    
    def preprocess_image(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocess an image for model inference.
        
        Args:
            image: PIL Image to preprocess
            
        Returns:
            Preprocessed image tensor ready for model inference
        """
        # Convert grayscale to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Apply transformations
        img_tensor = self.transform(image)
        
        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0)
        
        return img_tensor.to(self.device)
    
    def predict(
        self, 
        image: Image.Image, 
        top_k: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Predict the class of an image.
        
        Args:
            image: PIL Image to classify
            top_k: Number of top predictions to return (default: 5)
            
        Returns:
            List of tuples containing (class_label, probability) for top K predictions
            
        Raises:
            ValueError: If image is invalid or cannot be processed
        """
        try:
            # Load model if not already loaded
            self._load_model()
            
            # Preprocess image
            img_tensor = self.preprocess_image(image)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(img_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Get top K predictions
            top_probs, top_indices = torch.topk(probabilities, top_k)
            
            # Format results
            predictions = []
            for prob, idx in zip(top_probs, top_indices):
                class_name = self.class_labels[idx.item()]
                confidence = prob.item()
                predictions.append((class_name, confidence))
            
            logger.info(f"Prediction completed. Top class: {predictions[0][0]} ({predictions[0][1]:.2%})")
            return predictions
            
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")


# Global classifier instance (singleton pattern)
_classifier_instance: Optional[ImageClassifier] = None


def get_classifier() -> ImageClassifier:
    """
    Get the global classifier instance (singleton).
    
    Returns:
        ImageClassifier instance
    """
    global _classifier_instance
    if _classifier_instance is None:
        _classifier_instance = ImageClassifier()
    return _classifier_instance
