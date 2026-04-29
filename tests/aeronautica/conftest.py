import pytest

@pytest.fixture
def aeronave_valida():
    return {
        "id": "EC-MHU",
        "tipo": "Airbus A320neo",
        "aerolinea": "Iberia",
        "ciclos_totales": 4821,
        "horas_vuelo": 12430,
        "estado": "operativa",
        "proximo_mantenimiento": "2026-06-15"
    }

@pytest.fixture
def aeronave_fuera_de_servicio():
    return {
        "id": "EC-LZD",
        "tipo": "Boeing 737-800",
        "aerolinea": "Vueling",
        "ciclos_totales": 18200,
        "horas_vuelo": 41300,
        "estado": "AOG",
        "proximo_mantenimiento": "2026-05-01"
    }

@pytest.fixture
def vuelo_valido():
    return {
        "numero_vuelo": "IB3456",
        "origen": "MAD",
        "destino": "BCN",
        "aeronave_id": "EC-MHU",
        "hora_salida": "2026-05-10T08:30:00Z",
        "hora_llegada": "2026-05-10T09:45:00Z",
        "pasajeros": 156,
        "estado": "programado"
    }

@pytest.fixture
def orden_mantenimiento():
    return {
        "aeronave_id": "EC-MHU",
        "tipo": "check-A",
        "tecnico_id": 7,
        "descripcion": "Inspeccion de tren de aterrizaje y frenos",
        "prioridad": "alta",
        "fecha_inicio": "2026-06-15",
        "horas_estimadas": 8
    }