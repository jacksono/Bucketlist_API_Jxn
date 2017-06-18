"""Test cases for bucketlist routes."""

from tests.base_test import BaseTest
import json
from bucketlist.models import Bucketlist


class TestBucketlist(BaseTest):
    """Test cases for bucketlist routes."""

    def test_user_can_create_a_bucket_list(self):
        """Test that a user can create a bucketlist."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        r = self.app.post("/api/v1/auth/bucketlists/", data=self.bucketlist,
                          headers={"username": "user"})
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.bucketlist["title"],
                         Bucketlist.query.filter_by(
                             title="Love").first().title)

    def test_user_cannot_create_a_bucket_list_that_already_exists(self):
        """Test that a user cannot create a bucketlist that exists."""
        self.bucketlist = {"title": "Travel",
                           "description": "travel",
                           "created_by": 1}
        r = self.app.post("/api/v1/auth/bucketlists/", data=self.bucketlist,
                          headers={"username": "user"})
        message = json.loads(r.data.decode())
        self.assertIn("already exists", message["message"])

    def test_user_can_see_all_bucket_lists(self):
        """Test that a user can see all bucketlists."""
        r = self.app.get("/api/v1/auth/bucketlists/",
                         headers={"username": "user"})
        self.assertEqual(r.status_code, 200)
        message = json.loads(r.data.decode())
        self.assertIn("Travel", message[0]["name"])
        self.assertEqual(1, len(Bucketlist.query.all()))
