import unittest
from app import app


class LearnLoopAITest(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # ----------------------------
    # Home Page
    # ----------------------------
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # ----------------------------
    # AI Mentor Page
    # ----------------------------
    def test_mentor_page(self):
        response = self.client.get("/mentor")
        self.assertIn(response.status_code, [200, 302])

    # ----------------------------
    # Learning DNA Page
    # ----------------------------
    def test_learning_dna_page(self):
        response = self.client.get("/learning_dna")
        self.assertIn(response.status_code, [200, 302])

    # ----------------------------
    # Dashboard
    # ----------------------------
    def test_dashboard(self):
        response = self.client.get("/dashboard")
        self.assertIn(response.status_code, [200, 302])

    # ----------------------------
    # Quiz Page
    # ----------------------------
    def test_quiz_page(self):
        response = self.client.get("/quiz")
        self.assertIn(response.status_code, [200, 302])


if __name__ == "__main__":
    unittest.main()