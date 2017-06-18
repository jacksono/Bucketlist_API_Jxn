"""Contain the setup for other test cases."""
import nose
from flask_testing import TestCase
from bucketlist.app import db
from start import app
from bucketlist.models import User, Bucketlist, Item
from configuration.config import app_config


app.config.from_object(app_config["testing"])


class BaseTest(TestCase):
    """Base configurations for the testcases."""

    def create_app(self):
        """Return the app."""
        return app

    def setUp(self):
        """Fixture to create test database and set up test client."""
        self.app = app.test_client()
        db.create_all()
        user = User(username="user", password="password")

        bucketlist = Bucketlist(title="Travel",
                                description="Places I have to visit",
                                created_by=1)

        item = Item(name="Enjoy the beautiful beaches of Hawaii",
                    bucketlist_id=1)

        db.session.add(user)
        db.session.add(bucketlist)
        db.session.add(item)
        db.session.commit()

    def tearDown(self):
        """Fixture to destroy the database."""
        db.session.remove()
        db.drop_all()


if __name__ == "__main__":
    nose.start()
