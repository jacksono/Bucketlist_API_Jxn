"""Test user access to the app."""

from tests.base_test import BaseTest
import json
from bucketlist.models import User


class TestUser(BaseTest):
    """Create test cases for users functionality."""

    def get_token(self):
        """Return authentication token."""
        self.user = {"email": "user@bucketlist.com",
                     "password": "password"}
        r = self.app.post("/api/v1/auth/login",
                          data=self.user)
        output = json.loads(r.data.decode())
        token = output.get("token")
        return {"token": token}

    def test_user_can_register(self):
        """Tests if a new user can be registered."""
        self.user = {"username": "user1", "email": "user1@bucketlist.com",
                     "password": "password1"}
        r = self.app.post("/api/v1/auth/register", data=self.user)
        self.assertEqual(r.status_code, 201)
        message = json.loads(r.data.decode())
        self.assertIn("successfully registered", message["message"])
        self.assertEqual(self.user["username"],
                         User.query.filter_by(
                             username="user1").first().username)

    def test_user_cannot_register_with_an_existing_email(self):
        """Tests if a new user cannot register with an existing email."""
        self.user = {'username': 'user1', "email": "user@bucketlist.com",
                     "password": "password"}
        r = self.app.post("/api/v1/auth/register", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_error_message_if_username_not_provided_during_register(self):
        """Test for a message whn a username isn't given during registering."""
        self.user = {"email": "user@bucket.com", "password": "password"}
        r = self.app.post("/api/v1/auth/register", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a username",
                      message['message']['username'])

    def test_error_message_if_email_not_provided_during_register(self):
        """Test for a message when an email is'nt given during registering."""
        self.user = {"username": "user", "password": "password"}
        r = self.app.post("/api/v1/auth/register", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter an email",
                      message['message']['email'])

    def test_error_message_if_username_contains_special_characters(self):
        """Test for a message when a username contains special characters."""
        self.user = {"username": "user@#$", "email": "user@yahoo.com",
                     "password": "password"}
        r = self.app.post("/api/v1/auth/register", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("cannot contain special characters",
                      message['message'])

    def test_error_message_if_wrong_email_format_provided(self):
        """Test for a message when the email is not in a correct format."""
        self.user1 = {"username": "user", "email": "user",
                      "password": "password"}
        self.user2 = {"username": "user", "email": "user.com",
                      "password": "password"}
        self.user3 = {"username": "user", "email": "user*x.com",
                      "password": "password"}
        r1 = self.app.post("/api/v1/auth/register", data=self.user1)
        self.assertEqual(r1.status_code, 400)
        r2 = self.app.post("/api/v1/auth/register", data=self.user2)
        self.assertEqual(r2.status_code, 400)
        r3 = self.app.post("/api/v1/auth/register", data=self.user3)
        self.assertEqual(r3.status_code, 400)
        message1 = json.loads(r1.data.decode())
        message2 = json.loads(r2.data.decode())
        message3 = json.loads(r3.data.decode())
        self.assertIn("Invalid email",
                      message1['message'])
        self.assertIn("Invalid email",
                      message2['message'])
        self.assertIn("Invalid email",
                      message3['message'])

    def test_error_message_if_password_not_provided_during_register(self):
        """Test for a message when a user tries to register without a password.""" # noqa
        self.user = {"username": "user", "email": "user@bucketlist.com"}
        r = self.app.post("/api/v1/auth/register", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a password",
                      message["message"]["password"])

    def test_user_can_login(self):
        """Tests if a registered user can log in into Bucketlist."""
        self.user = {"email": "user@bucketlist.com", "password": "password"}
        r = self.app.post("/api/v1/auth/login", data=self.user)
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("Logged in successfully", message["message"])

    def test_error_message_shown_if_email_not_provided_during_login(self):
        """Test for a message when a user tries to login without an email."""
        self.user = {"password": "password"}
        r = self.app.post("/api/v1/auth/login", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter an email",
                      message["message"]["email"])

    def test_error_message_shown_if_password_not_provided_during_login(self):
        """Test for a message when a user tries to login without a password."""
        self.user = {"email": "user@bucketlist.com"}
        r = self.app.post("/api/v1/auth/login", data=self.user)
        message = json.loads(r.data.decode())
        self.assertIn("Please enter a password",
                      message["message"]["password"])

    def test_error_message_if_wrong_password_is_provided_during_login(self):
        """Test for a message when a user tries to login with a wrong password.""" # noqa
        self.user = {"email": "user@bucketlist.com", "password": "pass"}
        r = self.app.post("/api/v1/auth/login", data=self.user)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Incorrect password",
                      message["message"])

    def test_error_message_if_login_email_is_not_registered(self):
        """Test for a message when a user tries to login with an email that is not registered."""  # noqa
        self.user = {"email": "user1@bucket.com", "password": "password"}
        r = self.app.post("/api/v1/auth/login", data=self.user)
        self.assertEqual(r.status_code, 404)
        message = json.loads(r.data.decode())
        self.assertIn("That email is not yet registered",
                      message["message"])

    def test_user_can_change_username(self):
        """Tests if a registered user can change their username."""
        self.user = {"username": "user1"}
        r = self.app.put("/api/v1/auth/name", data=self.user,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("Username changed", message["message"])

    def test_user_cannot_change_to_the_current_username(self):
        """Tests if a registered user can change their username."""
        self.user = {"username": "user"}
        r = self.app.put("/api/v1/auth/name", data=self.user,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Use a new username", message["message"])
