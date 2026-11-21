import unittest
from fastapi.testclient import TestClient
from app.main import app

class HealthEndpointTestCase(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("capabilities", data)
        self.assertIn("en", data["capabilities"]["supported_languages"])
        self.assertIn("hi", data["capabilities"]["supported_languages"])
        self.assertIn("pa", data["capabilities"]["supported_languages"])

    def test_root_endpoint(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("health_check", data)

if __name__ == "__main__":
    unittest.main()
