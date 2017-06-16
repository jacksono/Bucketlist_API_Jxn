"""Test home route."""

from flask_testing import TestCase
from start import app
from configuration.config import app_config
import json

app.config.from_object(app_config["testing"])


class TestHomeRoute(TestCase):
    """Class to hold test cases for the home route."""

    def create_app(self):
        """ Returns app """
        return app

    def setUp(self):
        """ Create test database and set up test client """
        self.app = app.test_client()

    def test_home_route_shows_correct_message(self):
            """Test response to the home route."""
            r = self.app.get("/api/v1/")
            self.assertEqual(r.status_code, 200)
            output = json.loads(r.data.decode())
            self.assertEqual(output,
                             {"message": "This is the Bucketlist"
                              " API, You are WELCOME!!."
                              " To use the API please register or login"})
