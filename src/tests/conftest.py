import pytest
import sys
import os
from unittest.mock import patch

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture para el cliente de testing de FastAPI"""
    return TestClient(app)


@pytest.fixture
def mock_database_session():
    """Mock de la sesión de base de datos"""
    with patch("src.infrastructure.db.get_session") as mock_session:
        yield mock_session


@pytest.fixture
def mock_location_service():
    """Mock del servicio de ubicaciones"""
    with patch("src.services.location.LocationService") as mock_service:
        yield mock_service


@pytest.fixture
def mock_flight_repository():
    """Mock del repositorio de vuelos"""
    with patch("src.repository.flight.FlightRepository") as mock_repo:
        yield mock_repo
