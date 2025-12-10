"""
Pytest configuration and fixtures.

This file is automatically loaded by pytest and provides
shared fixtures for all test files.
"""

import pytest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set test environment to avoid downloading huge models in CI
os.environ['TORCH_HOME'] = os.path.join(os.path.dirname(__file__), '.torch_cache')
os.environ['MODEL_DEVICE'] = 'cpu'  # Force CPU in tests for speed


@pytest.fixture(autouse=True)
def reset_singleton():
    """Reset the global classifier singleton between tests."""
    from app.models import classifier
    classifier._classifier_instance = None
    yield
    classifier._classifier_instance = None)
