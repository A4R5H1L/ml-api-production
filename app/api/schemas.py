"""
Pydantic schemas for request/response validation.

This module defines all data models used for API request and response validation,
ensuring type safety and automatic documentation.
"""

from pydantic import BaseModel, Field
from typing import List, Tuple


class PredictionResult(BaseModel):
    """
    Single prediction result with class and confidence.
    
    Attributes:
        class_name: The predicted class label
        confidence: Confidence score between 0 and 1
    """
    class_name: str = Field(..., description="Predicted class label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")


class PredictionResponse(BaseModel):
    """
    Response model for prediction endpoint.
    
    Attributes:
        success: Whether the prediction was successful
        predictions: List of top predictions with confidence scores
        message: Optional message (e.g., for errors)
    """
    success: bool = Field(..., description="Whether prediction was successful")
    predictions: List[PredictionResult] = Field(..., description="List of predictions")
    message: str = Field(default="", description="Additional message or error details")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "success": True,
                "predictions": [
                    {"class_name": "golden_retriever", "confidence": 0.87},
                    {"class_name": "labrador", "confidence": 0.08},
                    {"class_name": "dog", "confidence": 0.03}
                ],
                "message": ""
            }
        }


class HealthResponse(BaseModel):
    """
    Response model for health check endpoint.
    
    Attributes:
        status: Health status ('healthy' or 'unhealthy')
        version: API version
        model_loaded: Whether the ML model is loaded
    """
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Whether ML model is loaded")
    
    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "model_loaded": True
            }
        }


class ErrorResponse(BaseModel):
    """
    Standard error response model.
    
    Attributes:
        success: Always False for errors
        error: Error message
        detail: Additional error details
    """
    success: bool = Field(default=False, description="Always False for errors")
    error: str = Field(..., description="Error message")
    detail: str = Field(default="", description="Additional error details")
