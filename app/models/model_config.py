"""
Configuration for selecting different ML models.

Available models:
- resnet18: Fast, lightweight (default)
- resnet50: Better accuracy, moderate speed
- resnet101: Best accuracy, slower
- efficientnet_b0: Good balance of accuracy and speed
"""

import logging
from typing import Optional

import torch
import torchvision.models as models

logger = logging.getLogger(__name__)


class ModelConfig:
    """Configuration for different model architectures."""

    MODELS = {
        "resnet18": {
            "class": models.resnet18,
            "weights": models.ResNet18_Weights.IMAGENET1K_V1,
            "description": "Fast and lightweight",
        },
        "resnet50": {
            "class": models.resnet50,
            "weights": models.ResNet50_Weights.IMAGENET1K_V2,
            "description": "Better accuracy, moderate speed",
        },
        "resnet101": {
            "class": models.resnet101,
            "weights": models.ResNet101_Weights.IMAGENET1K_V2,
            "description": "Best accuracy, slower",
        },
        "efficientnet_b2": {
            "class": models.efficientnet_b2,
            "weights": models.EfficientNet_B2_Weights.IMAGENET1K_V1,
            "description": "Efficient and accurate",
        },
    }

    @classmethod
    def get_model(cls, model_name: str, device: str):
        """
        Get a model by name.

        Args:
            model_name: Name of the model (resnet18, resnet50, etc.)
            device: Device to load model on ('cuda' or 'cpu')

        Returns:
            Loaded PyTorch model
        """
        if model_name not in cls.MODELS:
            logger.warning(f"Unknown model {model_name}, falling back to resnet18")
            model_name = "resnet18"

        model_info = cls.MODELS[model_name]
        logger.info(f"Loading {model_name}: {model_info['description']}")

        model = model_info["class"](weights=model_info["weights"])
        model.to(device)
        model.eval()

        return model
