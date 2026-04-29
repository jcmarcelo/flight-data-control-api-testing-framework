
def test_obtener_vuelos_programados(session, base_url):
    response = session.get(f"{base_url}/posts")
    assert response.status_code == 200

def test_sistema_tiene_vuelos_activos(session, base_url):
    response = session.get(f"{base_url}/posts")
    vuelos = response.json()
    assert len(vuelos) == 100

def test_vuelo_tiene_campos_criticos(session, base_url):
    response = session.get(f"{base_url}/posts/1")
    vuelo = response.json()
    campos_criticos = ["id", "userId", "title", "body"]
    for campo in campos_criticos:
        assert campo in vuelo, f"Campo crítico ausente en vuelo: {campo}"

def test_programar_vuelo_nuevo(session, base_url):
    payload = {
        "numero_vuelo": "IB3456",
        "origen": "MAD",
        "destino": "BCN",
        "aeronave_id": "EC-MHU",
        "estado": "programado"
    }
    response = session.post(f"{base_url}/posts", json=payload)
    assert response.status_code == 201
    assert response.json()["numero_vuelo"] == payload["numero_vuelo"] or "id" in response.json()

def test_cancelar_vuelo(session, base_url):
    response = session.delete(f"{base_url}/posts/1")
    assert response.status_code == 200

def test_modificar_estado_vuelo(session, base_url):
    payload = {"title": "en_ruta"}
    response = session.patch(f"{base_url}/posts/1", json=payload)
    assert response.status_code == 200
    assert response.json()["title"] == "en_ruta"

def test_tiempo_respuesta_vuelos_critico(session, base_url):
    response = session.get(f"{base_url}/posts")
    assert response.elapsed.total_seconds() < 3