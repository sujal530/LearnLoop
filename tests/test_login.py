import unittest
from app import app


class LoginTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test_secret"
        self.client = app.test_client()

    # -----------------------------
    # Login Page Loads
    # -----------------------------
    def test_login_page(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # Register Page Loads
    # -----------------------------
    def test_register_page(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)

    # -----------------------------
    # Dashboard Requires Login
    # -----------------------------
    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard")
        self.assertEqual(response.status_code, 302)

    # -----------------------------
    # Mentor Requires Login
    # -----------------------------
    def test_mentor_requires_login(self):
        response = self.client.get("/mentor")
        self.assertEqual(response.status_code, 302)

    # -----------------------------
    # Logout Redirects
    # -----------------------------
    def test_logout(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()