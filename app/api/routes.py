"""
API routes and endpoints.

This module defines all API endpoints including health checks and
the main prediction endpoint for image classification.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from PIL import Image
import io
import logging

from app.api.schemas import PredictionResponse, PredictionResult, HealthResponse, ErrorResponse
from app.models.classifier import get_classifier
from app.core.config import settings

logger = logging.getLogger(__name__)

# Create API router
router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the API and model",
    tags=["Health"]
)
async def health_check():
    """
    Health check endpoint.
    
    Returns the health status of the API, including whether
    the ML model is loaded and ready for predictions.
    
    Returns:
        HealthResponse with status information
    """
    classifier = get_classifier()
    
    return HealthResponse(
        status="healthy",
        version=settings.api_version,
        model_loaded=classifier.model is not None
    )


@router.post(
    "/predict",
    response_model=PredictionResponse,
    summary="Image Classification",
    description="Upload an image to get classification predictions",
    tags=["Prediction"],
    responses={
        200: {
            "description": "Successful prediction",
            "model": PredictionResponse
        },
        400: {
            "description": "Invalid image or request",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def predict_image(
    file: UploadFile = File(..., description="Image file to classify"),
    top_k: int = 5
):
    """
    Predict the class of an uploaded image.
    
    This endpoint accepts an image file and returns the top K predictions
    with their confidence scores using a pre-trained ResNet-18 model.
    
    Args:
        file: Uploaded image file (JPEG, PNG, etc.)
        top_k: Number of top predictions to return (default: 5, max: 10)
        
    Returns:
        PredictionResponse with top K predictions and confidence scores
        
    Raises:
        HTTPException: If the image is invalid or prediction fails
    """
    # Validate top_k parameter
    if top_k < 1 or top_k > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="top_k must be between 1 and 10"
        )
    
    # Validate file type
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type: {file.content_type}. Please upload an image."
        )
    
    try:
        # Read and validate image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        logger.info(
            f"Processing image: {file.filename}, size: {image.size}, mode: {image.mode}"
        )
        
        # Get classifier and make prediction
        classifier = get_classifier()
        predictions = classifier.predict(image, top_k=top_k)
        
        # Format response
        prediction_results = [
            PredictionResult(class_name=class_name, confidence=confidence)
            for class_name, confidence in predictions
        ]
        
        logger.info(
            f"Prediction successful for {file.filename}. "
            f"Top prediction: {predictions[0][0]} ({predictions[0][1]:.2%})"
        )
        
        return PredictionResponse(
            success=True,
            predictions=prediction_results,
            message=f"Successfully classified {file.filename}"
        )
        
    except Exception as e:
        logger.error(f"Prediction failed for {file.filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}"
        )
