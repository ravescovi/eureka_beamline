"""Test module for IOC analyzer router.

This module contains tests for the IOC analyzer router endpoints and models.
"""

from typing import TYPE_CHECKING, Dict, Any
import pytest
from fastapi.testclient import TestClient
from ..main import app
from ..routers.ioc_router import IOCAnalyzerInput, IOCAnalyzerOutput

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from pytest_mock import MockerFixture

client = TestClient(app)

@pytest.fixture
def mock_ioc_analyzer(mocker: "MockerFixture") -> None:
    """Fixture to mock IOC analyzer functionality.
    
    Args:
        mocker: Pytest mocker fixture.
    """
    # TODO: Implement mock for IOC analyzer
    pass

def test_analyze_ioc_success(mock_ioc_analyzer: None) -> None:
    """Test successful IOC analysis.
    
    Args:
        mock_ioc_analyzer: Fixture that mocks IOC analyzer functionality.
    """
    input_data = {
        "ioc_name": "test_ioc",
        "config_file": "/path/to/config.yaml",
        "options": {
            "include_dependencies": True,
            "validate_config": True
        }
    }
    
    response = client.post("/agents/ioc-analyzer", json=input_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["message"] == "Successfully analyzed IOC: test_ioc"
    assert data["details"]["ioc_name"] == "test_ioc"
    assert data["details"]["config_file"] == "/path/to/config.yaml"

def test_analyze_ioc_invalid_input() -> None:
    """Test IOC analysis with invalid input."""
    input_data = {
        "ioc_name": "",  # Empty IOC name should fail validation
        "config_file": "/path/to/config.yaml"
    }
    
    response = client.post("/agents/ioc-analyzer", json=input_data)
    assert response.status_code == 422  # Validation error

def test_analyze_ioc_missing_required() -> None:
    """Test IOC analysis with missing required fields."""
    input_data = {
        "ioc_name": "test_ioc"
        # Missing config_file should fail validation
    }
    
    response = client.post("/agents/ioc-analyzer", json=input_data)
    assert response.status_code == 422  # Validation error 