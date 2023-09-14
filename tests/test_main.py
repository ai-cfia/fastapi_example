import time
import unittest

from fastapi.testclient import TestClient

from src.main import app


class TestFastAPIApp(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("current_time", response.json())

    def test_query_performance(self):
        start_time = time.time()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        elapsed_time = time.time() - start_time
        self.assertTrue(elapsed_time < 0.200)

    # TODO: tests
