class TestOrdenesMantenimiento:
    def test_crear_orden_mantenimiento(self, session, base_url, orden_mantenimiento):
        response = session.post(f"{base_url}/posts", json=orden_mantenimiento)
        assert response.status_code == 201

    def test_orden_creada_tiene_id(self, session, base_url, orden_mantenimiento):
        response = session.post(f"{base_url}/posts", json=orden_mantenimiento)
        assert "id" in response.json()

    def test_consultar_ordenes_activas(self, session, base_url):
        response = session.get(f"{base_url}/posts")
        assert response.status_code == 200
        ordenes = response.json()
        assert len(ordenes) > 0

    def test_tiempo_respuesta_mantenimiento(self, session, base_url):
        response = session.get(f"{base_url}/posts")
        assert response.elapsed.total_seconds() < 2.0


class TestAsignacionTecnicos:
    def test_obtener_tecnicos_disponibles(self, session, base_url):
        response = session.get(f"{base_url}/users")
        assert response.status_code == 200
        tecnicos = response.json()
        assert len(tecnicos) > 0

    def test_tecnico_tiene_datos_contacto(self, session, base_url):
        response = session.get(f"{base_url}/users/1")
        tecnico = response.json()
        assert "email" in tecnico
        assert "phone" in tecnico

    def test_asignar_tecnico_a_orden(self, session, base_url, orden_mantenimiento):
        payload = {"userId": 7, "title": "check-A EC-MHU", "body": orden_mantenimiento["descripcion"]}
        response = session.post(f"{base_url}/posts", json=payload)
        assert response.status_code == 201
        assert response.json()["userId"] == 7

    def test_cerrar_orden_mantenimiento(self, session, base_url):
        payload = {"title": "COMPLETADO - check-A EC-MHU"}
        response = session.patch(f"{base_url}/posts/1", json=payload)
        assert response.status_code == 200
        assert "COMPLETADO" in response.json()["title"]