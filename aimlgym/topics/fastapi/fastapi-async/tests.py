"""Tests for FA-14 Async Endpoints and External Services.

Run:  python -m unittest tests -v
By default the reference solution is tested. To test a learner submission,
set AIMLGYM_TARGET to the module name (e.g. AIMLGYM_TARGET=starter).
"""
import importlib
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
S = importlib.import_module(os.environ.get("AIMLGYM_TARGET", "solution"))


import asyncio

from fastapi.testclient import TestClient


class FakeWeather:
    def __init__(self, temps):
        self.temps = temps
        self.active = 0
        self.peak = 0

    async def temperature(self, city):
        self.active += 1
        self.peak = max(self.peak, self.active)
        await asyncio.sleep(0)
        self.active -= 1
        if city == "hang":
            await asyncio.Event().wait()
        if city == "broken":
            raise ConnectionError("upstream down")
        if city not in self.temps:
            raise LookupError(city)
        return self.temps[city]


class FastSettings:
    timeout = 0.05


class TestAsyncEndpoints(unittest.TestCase):
    def setUp(self):
        self.fake = FakeWeather({"paris": 18.5, "oslo": 4.0, "delhi": 31.0})
        self.app = S.create_app()
        self.app.dependency_overrides[S.get_weather] = lambda: self.fake
        self.app.dependency_overrides[S.get_settings] = lambda: FastSettings()
        self.client = TestClient(self.app)

    def test_single_ok(self):
        self.assertEqual(self.client.get("/weather/paris").json(), {"city": "paris", "temperature": 18.5})

    def test_single_errors(self):
        self.assertEqual(self.client.get("/weather/hang").status_code, 504)
        self.assertEqual(self.client.get("/weather/atlantis").status_code, 404)
        r = self.client.get("/weather/broken")
        self.assertEqual((r.status_code, r.json()), (502, {"detail": "Weather service error"}))

    def test_many_in_order(self):
        r = self.client.get("/weather", params=[("city", "oslo"), ("city", "paris"), ("city", "delhi")])
        self.assertEqual(r.json(), [{"city": "oslo", "temperature": 4.0}, {"city": "paris", "temperature": 18.5},
                                    {"city": "delhi", "temperature": 31.0}])

    def test_many_runs_concurrently(self):
        self.client.get("/weather", params=[("city", "oslo"), ("city", "paris"), ("city", "delhi")])
        self.assertEqual(self.fake.peak, 3)

    def test_many_partial_failures(self):
        r = self.client.get("/weather", params=[("city", "paris"), ("city", "hang"), ("city", "x"), ("city", "broken")])
        self.assertEqual(r.json(), [{"city": "paris", "temperature": 18.5}, {"city": "hang", "error": "timeout"},
                                    {"city": "x", "error": "unknown city"}, {"city": "broken", "error": "service error"}])

    def test_requires_city(self):
        self.assertEqual(self.client.get("/weather").status_code, 422)

    def test_real_service_never_used_in_tests(self):
        with self.assertRaises(RuntimeError):
            asyncio.run(S.WeatherService().temperature("paris"))
        self.assertEqual(S.get_settings().timeout, 1.0)


if __name__ == "__main__":
    unittest.main()
