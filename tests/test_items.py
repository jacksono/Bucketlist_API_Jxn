"""Testacases for functionality involving items."""
from tests.base_test import BaseTest
import json
from bucketlist.models import Item


class TestItem(BaseTest):
    """Test items routes."""

    def get_token(self):
        """Return authentication token."""
        self.user = {"username": "user",
                     "password": "password"}
        r = self.app.post("/api/v1/auth/login/",
                          data=self.user)
        output = json.loads(r.data.decode())
        token = output.get("token")
        return {"token": token}

    def test_can_add_new_item(self):
        """Tests if a user can add a new item in a bucketlist."""
        self.item = {"name": "Go to Hawaii", "done": "True",
                     "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 201)
        message = json.loads(r.data.decode())
        self.assertIn("created successfully", message["message"])

    def test_shows_message_when_item_already_exists(self):
        """Tests that a message is shown when an item already exists."""
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "done": "True", "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_user_can_update_a_bucketlist_item(self):
        """Tests that a user can update an existing bucketlist item."""
        self.item = {"name": "New Item", "bucketlist_id": 1, "done": "True"}
        r = self.app.put("/api/v1/bucketlists/1/items/1", data=self.item,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Item.query.filter_by(name="New Item").first())
        self.assertFalse(Item.query.filter_by(
            name="Enjoy the beautiful beaches of Hawaii").first())

    def test_message_when_user_updates_to__name_that_already_exists(self):
        """Tests for an error message shown when a user tries to update to a item name which already exists.""" # noqa
        self.item = {"name": "Go to Hawaii", "done": "True",
                     "buckeltist_id": 1}
        self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                      headers=self.get_token())
        self.item2 = {"name": "Enjoy the beautiful beaches of Hawaii",
                      "bucketlist_id": 1, "done": "True"}
        r = self.app.put("/api/v1/bucketlists/1/items/2", data=self.item2,
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_message_when_user_updates_an_item_that_doesnot_exists(self):
        """Tests for an error message shown when a user tries to update an item which doesnot exist.""" # noqa
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "bucketlist_id": 1, "done": "True"}
        r = self.app.put("/api/v1/bucketlists/1/items/2", data=self.item,
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertIn("doesnot exist", message["message"])

    def test_message_when_user_updates_a_bucketlist_that_has_no_items(self):
        """Tests for an error message when a user tries to update a bucketlist which has no items.""" # noqa
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princcess",
                           "created_by": 1}
        self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                      headers=self.get_token())
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "bucketlist_id": 1, "done": "True"}
        r = self.app.put("/api/v1/bucketlists/2/items/1", data=self.item,
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertIn("has no items", message["message"])

    def test_user_can_delete_a_bucketlist_item(self):
        """Tests that a user can delete an existing bucketlist item."""
        r = self.app.delete("/api/v1/bucketlists/1/items/1",
                            headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertIn("deleted succesfully", message["message"])
        self.assertFalse(Item.query.all())
