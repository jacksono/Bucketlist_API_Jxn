"""Test user access to the app."""


from tests.base_test import BaseTest
import json
from bucketlist.models import User


class TestUser(BaseTest):
    """Create test cases for users functionality."""

    def test_user_can_register(self):
        """Tests if a new user can be registered as a user to Bucketlist."""
        self.user = {"username": "user3", "password": "password3"}
        r = self.app.post("/api/v1/auth/register/", data=self.user)
        self.assertEqual(r.status_code, 201)
        message = json.loads(r.data.decode())
        self.assertIn("new user", message["message"])
        self.assertEqual(self.user["username"],
                         User.query.filter_by(
                             username="user3").first().username)

    def test_user_cannot_register_with_an_existing_username(self):
        """Tests if a new user cannot registered with an existing username."""
        self.user = {"username": "user", "password": "password"}
        r = self.app.post("/api/v1/auth/register/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_error_message_if_username_not_provided_during_register(self):
        """Test for a message when a user tries to register without a username.""" # noqa
        self.user = {"password": "password"}
        r = self.app.post("/api/v1/auth/register/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a username",
                      message["message"]["username"])

    def test_error_message_if_password_not_provided_during_register(self):
        """Test for a message when a user tries to register without a password.""" # noqa
        self.user = {"username": "user"}
        r = self.app.post("/api/v1/auth/register/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a password",
                      message["message"]["password"])

    def test_user_can_login(self):
        """Tests if a registered user can log in into Bucketlist."""
        self.user = {"username": "user", "password": "password"}
        r = self.app.post("/api/v1/auth/login/", data=self.user)
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("Logged in successfully", message["message"])

    def test_error_message_shown_if_username_not_provided_during_login(self):
        """Test for a message when a user tries to login without a username."""
        self.user = {"password": "password"}
        r = self.app.post("/api/v1/auth/login/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a username",
                      message["message"]["username"])

    def test_error_message_shown_if_password_not_provided_during_login(self):
        """Test for a message when a user tries to login without a password."""
        self.user = {"username": "user"}
        r = self.app.post("/api/v1/auth/login/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a password",
                      message["message"]["password"])

    def test_error_message_if_wrong_password_is_provided_during_login(self):
        """Test for a message when a user tries to login with a wrong password.""" # noqa
        self.user = {"username": "user", "password": "pass"}
        r = self.app.post("/api/v1/auth/login/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("Incorrect password",
                      message["message"])

    def test_error_message_if_wrong_username_is_provided_during_login(self):
        """Test for a message when a user tries to login with a wrong username.""" # noqa
        self.user = {"username": "user1", "password": "password"}
        r = self.app.post("/api/v1/auth/login/", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("User not found",
                      message["message"])
