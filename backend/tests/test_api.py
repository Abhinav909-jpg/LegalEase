import unittest
from fastapi.testclient import TestClient
from app.main import app

class LegalEaseAPITestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_health_check(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("capabilities", data)

    def test_02_get_schemes(self):
        response = self.client.get("/api/schemes")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 4)
        
        # Test search filter
        response_punjab = self.client.get("/api/schemes?state=Punjab")
        self.assertEqual(response_punjab.status_code, 200)
        schemes_punjab = response_punjab.json()
        self.assertTrue(any("Punjab" in s["name"] for s in schemes_punjab))

    def test_03_get_scheme_by_id(self):
        response = self.client.get("/api/schemes/pm-usp-csss")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "pm-usp-csss")
        self.assertIn("eligibility", data)
        self.assertIn("required_documents", data)
        self.assertIn("scholarships.gov.in", data["source_url"])

    def test_04_eligibility_engine_eligible(self):
        # Eligible Punjab SC student
        payload = {
            "state": "Punjab",
            "category": "SC",
            "family_income": 180000,
            "education": "Undergraduate"
        }
        response = self.client.post("/api/eligibility/check", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(data["total_evaluated"], 0)
        punjab_eval = next((r for r in data["results"] if r["scheme_id"] == "punjab-post-matric-sc"), None)
        self.assertIsNotNone(punjab_eval)
        self.assertEqual(punjab_eval["match_status"], "ELIGIBLE")
        self.assertEqual(punjab_eval["match_percentage"], 100)

    def test_05_eligibility_engine_ineligible(self):
        # High income and General category should fail Punjab SC post matric
        payload = {
            "state": "Punjab",
            "category": "General",
            "family_income": 800000,
            "education": "Undergraduate"
        }
        response = self.client.post("/api/eligibility/check", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        punjab_eval = next((r for r in data["results"] if r["scheme_id"] == "punjab-post-matric-sc"), None)
        self.assertIsNotNone(punjab_eval)
        self.assertEqual(punjab_eval["match_status"], "INELIGIBLE")
        self.assertGreater(len(punjab_eval["failed_conditions"]), 0)

    def test_06_documents_list(self):
        response = self.client.get("/api/documents")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_07_rag_chat_grounded(self):
        # Query about Central Sector Scheme income limit
        payload = {
            "message": "What is the parental family income ceiling for the PM-USP Central Sector Scholarship?",
            "language": "en"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)
        self.assertIn("citations", data)
        # Should have found citations with page numbers
        self.assertGreater(len(data["citations"]), 0)
        first_citation = data["citations"][0]
        self.assertIn("document_name", first_citation)
        self.assertIn("page_number", first_citation)

    def test_08_rag_chat_hindi(self):
        payload = {
            "message": "पंजाब पोस्ट मैट्रिक छात्रवृत्ति के लिए कौन से दस्तावेज आवश्यक हैं?",
            "language": "hi"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["language"], "hi")
        self.assertGreater(len(data["citations"]), 0)

    def test_09_rag_chat_unverified(self):
        # Query about an invented non-existent scheme
        payload = {
            "message": "What is the grant amount for the Galactic Mars Flying Scholarship 2099?",
            "language": "en"
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)

if __name__ == "__main__":
    unittest.main()
