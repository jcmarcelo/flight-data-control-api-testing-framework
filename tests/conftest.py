import pytest
import requests

# API simulada para el sistema de control de flotas aeronáuticas
# En producción apuntaría a: https://api.flota-aerea.com
BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def session():
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "X-Sistema": "FlotaAerea-QA",        # cabecera que identificaría el sistema
        "X-Version": "1.0"
    })
    return s