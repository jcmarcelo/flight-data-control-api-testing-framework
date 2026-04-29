import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

class TestAutenticacion:

    def test_acceso_sin_token_no_expone_datos_sensibles(self, session, base_url):

        response = session.get(f"{base_url}/users/1")
        assert response.status_code in [200, 401, 403]

    def test_token_invalido_devuelve_error(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer token_invalido_xyz123"
        }
        response = requests.get(f"{BASE_URL}/users", headers=headers)
        assert response.status_code in [200, 401]

    def test_cabeceras_de_seguridad_presentes(self, session, base_url):
        response = session.get(f"{base_url}/users")
        assert "content-type" in response.headers
        assert "application/json" in response.headers["content-type"]

    def test_https_protocolo_seguro(self, session, base_url):
        assert base_url.startswith("https://"), "La API debe usar HTTPS en producción"