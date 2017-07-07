"""Testacases for functionality involving items."""
from tests.base_test import BaseTest
import json
from bucketlist.models import Item
from bucketlist.item_routes import get_item_by_id


class TestItem(BaseTest):
    """Test items routes."""

    def get_token(self):
        """Return authentication token."""
        self.user = {"email": "user@bucketlist.com",
                     "password": "password"}
        r = self.app.post("/api/v1/auth/login",
                          data=self.user)
        output = json.loads(r.data.decode())
        token = output.get("token")
        return {"token": token}

    def test_can_add_new_item(self):
        """Tests if a user can add a new item in a bucketlist."""
        self.item = {"name": "Go to Hawaii", "done": "n",
                     "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 201)
        message = json.loads(r.data.decode())
        self.assertIn("created successfully", message["message"])

    def test_error_when_missing_name_or_status(self):
        """Tests for error message when the name or status is missing."""
        self.item = {"name": "", "done": "",
                     "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("Name and/or Status can not be empty", message["message"])

    def test_shows_message_when_item_already_exists(self):
        """Tests that a message is shown when an item already exists."""
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "done": "Y", "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_user_can_update_a_bucketlist_item(self):
        """Tests that a user can update an existing bucketlist item."""
        self.item = {"name": "New Item", "bucketlist_id": 1, "done": "y"}
        r = self.app.put("/api/v1/bucketlists/1/items/1", data=self.item,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Item.query.filter_by(name="New Item").first())
        self.assertFalse(Item.query.filter_by(
            name="Enjoy the beautiful beaches of Hawaii").first())

    def test_user_cannot_update_a_bucketlist_item_with_the_old_name(self):
        """Tests that a user can update an existing bucketlist item."""
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "bucketlist_id": 1, "done": "n"}
        r = self.app.put("/api/v1/bucketlists/1/items/1", data=self.item,
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 200)
        self.assertIn("Use a new name", message["message"])

    def test_message_when_user_updates_to_name_that_already_exists(self):
        """Tests for an error message.

        shown when a user tries to update to a item name which already exists.
        """
        self.item = {"name": "Go to Hawaii", "done": "y",
                     "buckeltist_id": 1}
        self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                      headers=self.get_token())
        self.item2 = {"name": "Enjoy the beautiful beaches of Hawaii",
                      "bucketlist_id": 1, "done": "y"}
        r = self.app.put("/api/v1/bucketlists/1/items/2", data=self.item2,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_message_when_user_updates_an_item_that_doesnot_exists(self):
        """Tests for an error message shown when a user tries to update an item which doesnot exist.""" # noqa
        self.item = {"name": "Enjoy the beautiful beaches of Hawaii",
                     "bucketlist_id": 1, "done": "n"}
        r = self.app.put("/api/v1/bucketlists/1/items/2", data=self.item,
                         headers=self.get_token())
        r2 = self.app.put("/api/v1/bucketlists/2/items/1", data=self.item,
                          headers=self.get_token())
        message = json.loads(r.data.decode())
        message2 = json.loads(r2.data.decode())
        self.assertEqual(r.status_code, 404)
        self.assertEqual(r2.status_code, 404)
        self.assertIn("does not exist", message["message"])
        self.assertIn("does not exist", message2["message"])

    def test_message_when_user_updates_a_bucketlist_that_has_no_items(self):
        """Tests for an error message when a user tries to update a bucketlist which has no items.""" # noqa
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princcess",
                           "created_by": '1'}
        self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                      headers=self.get_token())
        self.item = {"name": "Enjoy the beautiful sands of Hawaii",
                     "bucketlist_id": 1, "done": "True"}
        r = self.app.put("/api/v1/bucketlists/2/items/1", data=self.item,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 404)
        message = json.loads(r.data.decode())
        self.assertIn("has no items", message["message"])

    def test_user_can_delete_a_bucketlist_item(self):
        """Tests that a user can delete an existing bucketlist item."""
        r = self.app.delete("/api/v1/bucketlists/1/items/1",
                            headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 200)
        self.assertIn("deleted succesfully", message["message"])
        self.assertFalse(Item.query.all())

    def test_user_cannot_delete_a_nonexisting_bucketlist_item(self):
        """Tests that a user can delete an existing bucketlist item."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                      headers=self.get_token())
        r1 = self.app.delete("/api/v1/bucketlists/1/items/2",
                             headers=self.get_token())
        r2 = self.app.delete("/api/v1/bucketlists/2/items/1",
                             headers=self.get_token())
        r3 = self.app.delete("/api/v1/bucketlists/3/items/1",
                             headers=self.get_token())
        message1 = json.loads(r1.data.decode())
        message2 = json.loads(r2.data.decode())
        message3 = json.loads(r3.data.decode())
        self.assertEqual(r1.status_code, 404)
        self.assertEqual(r2.status_code, 404)
        self.assertEqual(r3.status_code, 404)
        self.assertIn("item doesnot exist", message1["message"])
        self.assertIn("does not  have any items", message2["message"])
        self.assertIn("Bucketlist does not exist", message3["message"])

    def test_item_done_field_accepts_y_or_n_only_in_post(self):
        """Tests that the item done field accpets Y/y and N/n only in post."""
        self.item = {"name": "Go to Hawaii", "done": "True",
                     "buckeltist_id": 1}
        r = self.app.post("/api/v1/bucketlists/1/items/", data=self.item,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("use Y/N or y/n", message["message"])

    def test_item_done_field_accepts_y_or_n_only_in_put(self):
        """Tests that the item done field accpets Y/y and N/n only in put."""
        self.item = {"name": "Go to Hawaii", "done": "True",
                     "buckeltist_id": 1}
        r = self.app.put("/api/v1/bucketlists/1/items/1", data=self.item,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("use Y/N or y/n", message["message"])

    def test_user_can_get_all_bucketlist_items(self):
        """Tests that a user can get a list of all bucketlist items."""
        r = self.app.get("/api/v1/bucketlists/1/items/",
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 200)
        self.assertIn("Enjoy the beautiful", message["items"][0]["name"])

    def test_message_when_there_are_no_bucketlist_items(self):
        """Tests message shown when there are no items."""
        self.app.delete("/api/v1/bucketlists/1/items/1",
                        headers=self.get_token())
        r = self.app.get("/api/v1/bucketlists/1/items/",
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 200)
        self.assertIn("No items", message["message"])

    def test_message_when_the_bucketlist_doesnt_exist(self):
        """Tests message shown when the bucketlist doesnot exist."""
        r = self.app.get("/api/v1/bucketlists/2/items/",
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 404)
        self.assertIn("does not exist", message["message"])

    def test_get_item_by_id_works(self):
        """Tests if helper function works."""
        self.assertEqual(get_item_by_id(1, 1).name,
                         "Enjoy the beautiful beaches of Hawaii")

    def test_get_item_by_id_returns_none(self):
        """Tests if helper function returns none if item doesnt exist."""
        self.assertEqual(get_item_by_id(1, 2),
                         None)
        self.assertEqual(get_item_by_id(2, 1),
                         None)
