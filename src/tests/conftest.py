import pytest
import sys
import os

# Agregar el directorio src al path para los imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    """Fixture para el cliente de testing de FastAPI"""
    return TestClient(app)
