"""Test routes."""

from flask_testing import TestCase
from start import app
from configuration.config import app_config
import json

app.config.from_object(app_config["testing"])


class TestRoutes(TestCase):
    """Class to hold test cases for all routes and authorised access."""

    def create_app(self):
        """Return the app."""
        return app

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()

    def test_home_route_shows_correct_message(self):
            """Test response to the home route and the message displayed."""
            r = self.app.get("/api/v1/")
            self.assertEqual(r.status_code, 200)
            output = json.loads(r.data.decode())
            self.assertEqual(output,
                             {"message": "This is the Bucketlist"
                              " API, You are WELCOME!!."
                              " To use the API please register or login"})

    def test_invalid_route_shows_error_message(self):
            """Tests response to an invalid route."""
            r1 = self.app.get("/api/v1/x")
            r2 = self.app.get("/x")
            r3 = self.app.get("/login/x")
            output1 = json.loads(r1.data.decode())
            output2 = json.loads(r2.data.decode())
            output3 = json.loads(r3.data.decode())
            self.assertEqual(output1,
                             {"message": "Error: Wrong URL or Incorrect"
                              " request METHOD. Please check and try again"})
            self.assertEqual(output2,
                             {"message": "Error: Wrong URL or Incorrect"
                              " request METHOD. Please check and try again"})
            self.assertEqual(output3,
                             {"message": "Error: Wrong URL or Incorrect"
                              " request METHOD. Please check and try again"})

    def test_wrong_route_method_shows_error_message(self):
            """Tests response to a wrong route method ."""
            r1 = self.app.post("/api/v1/")
            r2 = self.app.get("/api/v1/auth/login")
            r3 = self.app.put("/api/v1/auth/register")
            output1 = json.loads(r1.data.decode())
            output2 = json.loads(r2.data.decode())
            output3 = json.loads(r3.data.decode())
            self.assertEqual(output1,
                             {"message": "Error: Wrong URL or Incorrect"
                              " request METHOD. Please check and try again"})
            self.assertEqual(output2,
                             {"message": "Error: Wrong URL or Incorrect"
                              " request METHOD. Please check and try again"})
            self.assertEqual(output3,
                             {"message": "Error: Wrong URL or Incorrect"
                              " request METHOD. Please check and try again"})

    def test_private_routes_not_accesible_without_a_token(self):
            """Tests that users can't access private routes without a token."""
            r1 = self.app.get("/api/v1/bucketlists/")
            r2 = self.app.post("/api/v1/bucketlists/")
            r3 = self.app.post("/api/v1/bucketlists/1/items/")
            output1 = json.loads(r1.data.decode())
            output2 = json.loads(r2.data.decode())
            output3 = json.loads(r3.data.decode())
            self.assertEqual(output1,
                             {"message": "Error: Please enter a token"})
            self.assertEqual(output2,
                             {"message": "Error: Please enter a token"})
            self.assertEqual(output3,
                             {"message": "Error: Please enter a token"})

    def test_error_message_shown_for_an_invalid_token(self):
            """Tests for an error message  when an invalid token is used."""
            r1 = self.app.get("/api/v1/bucketlists/",
                              headers={"token": "token"})
            output1 = json.loads(r1.data.decode())
            self.assertEqual(output1,
                             {"message": "Error: Invalid Token"})
