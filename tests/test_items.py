"""Testacases for functionality involving items."""
from tests.base_test import BaseTest
import json
from bucketlist.models import Item


class TestItem(BaseTest):
    """Test items routes."""

    def test_can_add_new_item(self):
        """Tests if a user can add a new item in a bucketlist."""
        self.item = {"name": "Go to Hawaii", "done": "True",
                     "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers={"username": "user", "bucketlist": "Travel"})
        self.assertEqual(r.status_code, 201)
        message = json.loads(r.data.decode())
        self.assertIn("created successfully", message["message"])

    def test_shows_message_when_item_already_exists(self):
        """Tests that a message is shown when an item already exists."""
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "done": "True", "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers={"username": "user"})
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])
