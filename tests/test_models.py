"""Test cases for models."""

from tests.base_test import BaseTest
from bucketlist.models import User, Bucketlist, Item


class TestModels(BaseTest):
    """Testcases for models."""

    def test_user_model_represents_object_by_user_name(self):
        """Test the __repr__ of the User model."""
        self.assertIn("user",
                      str(User.query.all()))

    def test_user_cannot_edit_password(self):
        """Test that the password field cannot be edited if accessed."""
        user = User.query.filter_by(username="user").first()
        with self.assertRaises(AttributeError):
            user.password()

    def test_user_model_verifies_password_correctly(self):
        """Test that a correct password is verified."""
        user = User.query.filter_by(username="user").first()
        self.assertTrue(user.verify_password("password"))

    def test_bucketlist_model_represents_object_by_title(self):
        """Test the __repr__ of the Bucketlist model."""
        self.assertIn("Travel",
                      str(Bucketlist.query.all()))

    def test_item_model_represents_object_by_name(self):
        """Test the __repr__ of the Item model."""
        self.assertIn("Enjoy",
                      str(Item.query.all()))
