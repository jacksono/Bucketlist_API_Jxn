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
