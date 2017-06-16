"""Test user access to the app."""

from tests.base_test import BaseTest
import json


class TestUser(BaseTest):
    """Create test cases for users functionality."""

    def test_user_can_login(self):
        """Test if a registered user can log in into Bucketlist."""
        self.user = {"username": "user", "password": "password"}
        r = self.app.post("/api/v1/auth/login/", data=self.user)
        self.assertEqual(r.status_code, 200)
        output = json.loads(r.data.decode())
        self.assertIn("Logged in successfully" in output["message"])
