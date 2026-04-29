def test_obtener_flota_completa(session, base_url):
    response = session.get(f"{base_url}/users")
    assert response.status_code == 200

def test_flota_devuelve_lista(session, base_url):
    response = session.get(f"{base_url}/users")
    flota = response.json()
    assert isinstance(flota, list)
    assert len(flota) > 0

def test_aeronave_tiene_campos_obligatorios(session, base_url):
    response = session.get(f"{base_url}/users/1")
    aeronave = response.json()
    campos = ["id", "name", "email", "phone"]
    for campo in campos:
        assert campo in aeronave, f"Campo obligatorio ausente: {campo}"

def test_registrar_aeronave_nueva(session, base_url):
    payload = {
        "matricula": "EC-MHU",
        "tipo": "Airbus A320neo",
        "aerolinea": "Iberia",
        "estado": "operativa"
    }
    response = session.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201

def test_tiempo_respuesta_flota_aceptable(session, base_url):
    response = session.get(f"{base_url}/users")
    assert response.elapsed.total_seconds() < 3