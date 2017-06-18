"""Test cases for bucketlist routes."""

from tests.base_test import BaseTest
import json
from bucketlist.models import Bucketlist


class TestBucketlist(BaseTest):
    """Test cases for bucketlist routes."""

    def test_user_can_create_a_bucket_list(self):
        """Test that a logged in iser can create a bucketlist."""
        self.bucketlist = {"title": "Love",
                           "description": "I want to marry a princess",
                           "created_by": 1}
        r = self.app.post("/api/v1/auth/bucketlists/", data=self.bucketlist)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(self.bucketlist["title"],
                         Bucketlist.query.filter_by(
                             title="Love").first().title)
