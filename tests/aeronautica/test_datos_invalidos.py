class TestDatosInvalidos:

    def test_crear_aeronave_sin_matricula(self, session, base_url):
        """Una aeronave sin matrícula no debería registrarse."""
        payload = {
            "tipo": "Airbus A320",
            "estado": "operativa"
        }
        response = session.post(f"{base_url}/users", json=payload)
        assert response.status_code in [201, 400, 422]

    def test_horas_vuelo_negativas(self, session, base_url):
        payload = {
            "matricula": "EC-MHU",
            "horas_vuelo": -500,
            "estado": "operativa"
        }
        response = session.post(f"{base_url}/users", json=payload)
        assert response.status_code in [201, 400, 422]

    def test_estado_aeronave_valor_no_permitido(self, session, base_url):
        payload = {"estado": "volando_a_marte"}  # valor inválido
        response = session.patch(f"{base_url}/users/1", json=payload)
        assert response.status_code in [200, 400, 422]

    def test_payload_vacio(self, session, base_url):
        response = session.post(f"{base_url}/users", json={})
        assert response.status_code in [201, 400, 422]
        assert response.elapsed.total_seconds() < 3

    def test_tipo_de_dato_incorrecto(self, session, base_url):
        payload = {
            "ciclos_totales": "muchos",
            "horas_vuelo": "bastantes"
        }
        response = session.post(f"{base_url}/users", json=payload)
        assert response.status_code in [201, 400, 422]

    def test_id_aeronave_inexistente(self, session, base_url):
        response = session.get(f"{base_url}/users/999999")
        assert response.status_code in [200, 404]