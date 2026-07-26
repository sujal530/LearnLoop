import unittest
from app import app


class QuizTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test_secret"
        self.client = app.test_client()

    # -----------------------------
    # Quiz Page Loads
    # -----------------------------
    def test_quiz_page(self):
        response = self.client.get("/quiz")
        self.assertIn(response.status_code, [200, 302])

    # -----------------------------
    # Quiz Requires Login
    # -----------------------------
    def test_quiz_requires_login(self):
        with self.client:
            self.client.get("/logout")
            response = self.client.get("/quiz")
            self.assertEqual(response.status_code, 302)

    # -----------------------------
    # Quiz Route Exists
    # -----------------------------
    def test_quiz_route_exists(self):
        response = self.client.get("/quiz", follow_redirects=True)
        self.assertNotEqual(response.status_code, 404)

    # -----------------------------
    # Invalid Quiz URL
    # -----------------------------
    def test_invalid_quiz_route(self):
        response = self.client.get("/quiz/invalid")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()