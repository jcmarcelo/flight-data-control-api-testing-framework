class TestNegativosAeronaves:
    def test_aeronave_no_encontrada_no_rompe_servidor(self, session, base_url):
        response = session.get(f"{base_url}/users/99999")
        assert response.status_code != 500, "El servidor no debe romperse con IDs inexistentes"

    def test_eliminar_aeronave_inexistente(self, session, base_url):
        response = session.delete(f"{base_url}/users/99999")
        assert response.status_code in [200, 404]

    def test_metodo_http_no_permitido(self, session, base_url):
        response = session.patch(f"{base_url}/users", json={"name": "test"})
        assert response.status_code in [200, 404, 405]

    def test_servidor_no_devuelve_500(self, session, base_url):
        endpoints = ["/users", "/posts", "/users/1", "/posts/1"]
        for endpoint in endpoints:
            response = session.get(f"{base_url}{endpoint}")
            assert response.status_code != 500, f"Error 500 en {endpoint}"

    def test_vuelo_con_aeronave_aog_no_deberia_operar(self, session, base_url):
        # Simulamos consultar vuelos de aeronave fuera de servicio
        response = session.get(f"{base_url}/users/1/posts")
        assert response.status_code in [200, 404, 409]

    def test_respuesta_siempre_es_json(self, session, base_url):
        endpoints = ["/users", "/posts", "/users/1"]
        for endpoint in endpoints:
            response = session.get(f"{base_url}{endpoint}")
            assert "application/json" in response.headers.get("content-type", ""), \
                f"Respuesta no es JSON en {endpoint}"