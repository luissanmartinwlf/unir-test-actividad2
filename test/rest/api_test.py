import http.client
import os
import unittest
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

BASE_URL = os.environ.get("BASE_URL")
DEFAULT_TIMEOUT = 2  # in secs


@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    # Funciones de ayuda

    def get(self, path):
        """Hace una peticion GET y devuelve (codigo HTTP, texto de la respuesta)."""
        url = f"{BASE_URL.rstrip('/')}{path}"
        try:
            response = urlopen(url, timeout=DEFAULT_TIMEOUT)
            return response.status, response.read().decode()
        except HTTPError as error:
            # urlopen lanza una excepcion con codigos 4xx/5xx: la capturamos
            return error.code, error.read().decode()

    def assert_ok(self, path, expected):
        status, body = self.get(path)
        self.assertEqual(status, http.client.OK, f"Error en la petición API a {path}")
        self.assertAlmostEqual(float(body), expected, delta=0.0000001)

    def assert_bad_request(self, path):
        status, _ = self.get(path)
        self.assertEqual(
            status, http.client.BAD_REQUEST, f"Se esperaba 400 en la peticion API a {path}"
        )

    # Raiz

    def test_api_hello(self):
        status, body = self.get("/")
        self.assertEqual(status, http.client.OK)
        self.assertIn("Hello", body)

    def test_api_unknown_route_returns_not_found(self):
        status, _ = self.get("/calc/unknown/1/2")
        self.assertEqual(status, http.client.NOT_FOUND)

    # Suma

    def test_api_add(self):
        self.assert_ok("/calc/add/2/2", 4)
        self.assert_ok("/calc/add/-2/2", 0)
        self.assert_ok("/calc/add/1.5/2", 3.5)

    def test_api_add_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/add/a/2")
        self.assert_bad_request("/calc/add/2/b")

    # Resta

    def test_api_substract(self):
        self.assert_ok("/calc/substract/5/3", 2)
        self.assert_ok("/calc/substract/2/5", -3)

    def test_api_substract_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/substract/a/2")
        self.assert_bad_request("/calc/substract/2/b")

    # Multiplicacion

    def test_api_multiply(self):
        self.assert_ok("/calc/multiply/2/3", 6)
        self.assert_ok("/calc/multiply/-2/3", -6)
        self.assert_ok("/calc/multiply/2.5/2", 5)

    def test_api_multiply_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/multiply/a/2")
        self.assert_bad_request("/calc/multiply/2/b")

    # Division

    def test_api_divide(self):
        self.assert_ok("/calc/divide/6/3", 2)
        self.assert_ok("/calc/divide/1/2", 0.5)

    def test_api_divide_fails_with_division_by_zero(self):
        self.assert_bad_request("/calc/divide/1/0")
        self.assert_bad_request("/calc/divide/1/0.0")

    def test_api_divide_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/divide/a/2")
        self.assert_bad_request("/calc/divide/2/b")

    # Potencia

    def test_api_power(self):
        self.assert_ok("/calc/power/2/3", 8)
        self.assert_ok("/calc/power/2/-1", 0.5)
        self.assert_ok("/calc/power/9/0.5", 3)

    def test_api_power_fails_with_invalid_values(self):
        self.assert_bad_request("/calc/power/0/-1")
        self.assert_bad_request("/calc/power/-8/0.5")

    def test_api_power_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/power/a/2")
        self.assert_bad_request("/calc/power/2/b")

    # Raiz cuadrada

    def test_api_sqrt(self):
        self.assert_ok("/calc/sqrt/4", 2)
        self.assert_ok("/calc/sqrt/0", 0)
        self.assert_ok("/calc/sqrt/2.25", 1.5)

    def test_api_sqrt_fails_with_negative_number(self):
        self.assert_bad_request("/calc/sqrt/-4")

    def test_api_sqrt_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/sqrt/a")

    # Logaritmo en base 10

    def test_api_log10(self):
        self.assert_ok("/calc/log10/100", 2)
        self.assert_ok("/calc/log10/1", 0)
        self.assert_ok("/calc/log10/0.1", -1)

    def test_api_log10_fails_with_zero_or_negative_number(self):
        self.assert_bad_request("/calc/log10/0")
        self.assert_bad_request("/calc/log10/-10")

    def test_api_log10_fails_with_nan_parameter(self):
        self.assert_bad_request("/calc/log10/a")
