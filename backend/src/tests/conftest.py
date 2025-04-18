"""Shared test fixtures and configuration.

This module contains pytest fixtures and configuration that are shared across
all test modules.
"""

from typing import TYPE_CHECKING, Generator
import pytest
from fastapi.testclient import TestClient
from eureka_beam.main import app

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Fixture that provides a FastAPI TestClient instance.
    
    Yields:
        TestClient: A FastAPI test client instance.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_env_vars(monkeypatch: pytest.MonkeyPatch) -> None:
    """Fixture that sets up mock environment variables for testing.
    
    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("OPENAI_API_KEY", "test-key") 