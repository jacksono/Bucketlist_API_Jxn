"""Test cases for bucketlist routes."""

from tests.base_test import BaseTest
import json
from bucketlist.models import Bucketlist
from bucketlist.bucketlist_routes import get_bucketlist_by_id


class TestBucketlist(BaseTest):
    """Test cases for bucketlist routes."""

    def get_token(self):
        """Return authentication token."""
        self.user = {"email": "user@bucketlist.com",
                     "password": "password"}
        r = self.app.post("/api/v1/auth/login",
                          data=self.user)
        output = json.loads(r.data.decode())
        token = output.get("token")
        return {"token": token}

    def test_user_can_create_a_bucket_list(self):
        """Test that a user can create a bucketlist."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        r = self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.bucketlist["title"],
                         Bucketlist.query.filter_by(
                             title="Love").first().title)

    def test_user_cannot_create_a_bucket_list_that_already_exists(self):
        """Test that a user cannot create a bucketlist that exists."""
        self.bucketlist = {"title": "Travel",
                           "description": "travel",
                           "created_by": 1}
        r = self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                          headers=self.get_token())
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_error_when_title_description_not_filled(self):
        """Test error when title or descriptionnot filled."""
        self.bucketlist = {"title": "",
                           "description": "",
                           "created_by": 1}
        r = self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                          headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 400)
        self.assertIn("Title and/or Description can not be empty",
                      message["message"])

    def test_user_can_see_all_bucket_lists(self):
        """Test that a user can see all bucketlists."""
        r = self.app.get("/api/v1/bucketlists/", headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("Travel", message["Bucketlists"][0]["name"])
        self.assertEqual(1, len(Bucketlist.query.all()))

    def test_message_shown_for_no_bucketlist_(self):
        """Test that a message is shown for no bucketlist."""
        self.app.delete("/api/v1/bucketlists/1",
                        headers=self.get_token())
        r = self.app.get("/api/v1/bucketlists/", headers=self.get_token())
        self.assertEqual(r.status_code, 404)
        message = json.loads(r.data.decode())
        self.assertIn("No bucketlist", message["message"])

    def test_can_get_single_bucket_list(self):
        """Tests that a single bucket list can be displayed."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                      headers=self.get_token())
        r = self.app.get("/api/v1/bucketlists/1",
                         headers=self.get_token())
        r2 = self.app.get("/api/v1/bucketlists/2",
                          headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r2.status_code, 200)
        message = json.loads(r.data.decode())
        message2 = json.loads(r2.data.decode())
        self.assertIn("Travel", message["name"])
        self.assertIn("No items yet", message2["items"][0]["message"])
        self.assertEqual(2, len(Bucketlist.query.all()))

    def test_cannot_get_single_bucket_list_if_it_doesnot_exist(self):
        """Tests cannot get a non existant bucketlist."""
        r = self.app.get("/api/v1/bucketlists/2",
                         headers=self.get_token())
        message = json.loads(r.data.decode())
        self.assertEqual(r.status_code, 404)
        self.assertIn("does not exist", message["message"])

    def test_user_can_update_a_bucketlist(self):
        """Tests if a user can update a bucketlist."""
        self.bucketlist = {"title": "Move",
                           "description": "Move around the world",
                           "created_by": 1}
        r = self.app.put("/api/v1/bucketlists/1", data=self.bucketlist,
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Bucketlist.query.filter_by(title="Move").first())
        self.assertFalse(Bucketlist.query.filter_by(title="Travel").first())

    def test_user_cannot_update_a_non_existant_bucketlist(self):
        """Tests that a user cannot delete a bucket list that doesnot exist."""
        r = self.app.put("/api/v1/bucketlists/2",
                         headers=self.get_token())
        self.assertEqual(r.status_code, 404)
        message = json.loads(r.data.decode())
        self.assertIn("Cannot update", message["message"])

    def test_user_cannot_update_with_same_title(self):
        """Tests that a user cannot update with same title."""
        self.bucketlist = {"title": "Travel",
                           "description": "Move around the world",
                           "created_by": 1}
        r = self.app.put("/api/v1/bucketlists/1",
                         headers=self.get_token(), data=self.bucketlist)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("use a new Title", message["message"])

    def test_user_cannot_update_with_to_an_existing_title(self):
        """Tests that a user cannot update with same title."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                      headers=self.get_token())
        self.bucketlist = {"title": "Travel",
                           "description": "Move around the world",
                           "created_by": 1}
        r = self.app.put("/api/v1/bucketlists/2",
                         headers=self.get_token(), data=self.bucketlist)
        self.assertEqual(r.status_code, 400)
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_user_can_delete_a_bucketlist(self):
        """Tests that a user can delete a bucketlist."""
        r = self.app.delete("/api/v1/bucketlists/1",
                            headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        self.assertEqual(0, len(Bucketlist.query.all()))

    def test_user_cannot_delete_a_non_existant_bucketlist(self):
        """Tests that a user cannot delete a bucket list that doesnot exist."""
        r = self.app.delete("/api/v1/bucketlists/2",
                            headers=self.get_token())
        self.assertEqual(r.status_code, 404)
        message = json.loads(r.data.decode())
        self.assertIn("does not exist", message["message"])

    def test_search_by_name_option_works(self):
        """Tests that a user can search for a bucketlist by name."""
        r = self.app.get("/api/v1/bucketlists/?q=Travel",
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("Travel", message["Bucketlists"][0]["name"])

    def test_pagination_option_shows_next_page(self):
        """Tests that a bucketlists are paginated."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        self.app.post("/api/v1/bucketlists/", data=self.bucketlist,
                      headers=self.get_token())
        r = self.app.get("/api/v1/bucketlists/?limit=1",
                         headers=self.get_token())
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertEqual("http://localhost/api/v1/bucketlists?limit=1&page=2",
                         message['Next Page'])

    def test_pagination_option_shows_previous_page(self):
        """Tests that a bucketlists are paginated."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        self.app.get("/api/v1/bucketlists/?limit=1",
                     headers=self.get_token())
        r = self.app.get("/api/v1/bucketlists?limit=1&page=2",
                         headers=self.get_token())
        self.assertEqual(r.status_code, 301)

    def test_get_bucketlist_by_id_returns_none(self):
        """Tests if helper function returns none if bucketlist doesnt exist."""
        self.app.delete("/api/v1/bucketlists/1",
                        headers=self.get_token())
        self.assertEqual(get_bucketlist_by_id(1),
                         None)
