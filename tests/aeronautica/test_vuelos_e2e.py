class TestProgramacionVuelos:
    def test_programar_vuelo_exitoso(self, session, base_url, vuelo_valido):
        response = session.post(f"{base_url}/posts", json=vuelo_valido)
        assert response.status_code == 201

    def test_vuelo_programado_tiene_id(self, session, base_url, vuelo_valido):
        response = session.post(f"{base_url}/posts", json=vuelo_valido)
        assert "id" in response.json()

    def test_consultar_vuelos_programados(self, session, base_url):
        response = session.get(f"{base_url}/posts")
        assert response.status_code == 200
        assert len(response.json()) > 0

    def test_consultar_vuelo_especifico(self, session, base_url):
        response = session.get(f"{base_url}/posts/1")
        vuelo = response.json()
        assert "id" in vuelo
        assert "title" in vuelo

    def test_tiempo_respuesta_vuelos_critico(self, session, base_url):
        response = session.get(f"{base_url}/posts")
        assert response.elapsed.total_seconds() < 1.5


class TestIntegridadVuelo:

    def test_vuelo_tiene_campos_criticos(self, session, base_url):
        response = session.get(f"{base_url}/posts/1")
        vuelo = response.json()
        campos_criticos = ["id", "userId", "title", "body"]
        for campo in campos_criticos:
            assert campo in vuelo, f"Campo crítico ausente en vuelo: {campo}"

    def test_modificar_estado_vuelo(self, session, base_url):
        payload = {"title": "en_ruta"}
        response = session.patch(f"{base_url}/posts/1", json=payload)
        assert response.status_code == 200
        assert response.json()["title"] == "en_ruta"

    def test_cancelar_vuelo(self, session, base_url):
        response = session.delete(f"{base_url}/posts/1")
        assert response.status_code == 200

    def test_vuelos_de_aeronave_especifica(self, session, base_url):
        response = session.get(f"{base_url}/users/1/posts")
        assert response.status_code == 200
        assert isinstance(response.json(), list)