"""
Pytest configuration and fixtures.

This file is automatically loaded by pytest and provides
shared fixtures for all test files.
"""

import os
import sys

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
