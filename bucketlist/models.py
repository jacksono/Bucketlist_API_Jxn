"""Module to create the models for the app."""

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bucketlist.app import db


class User(db.Model):
    """Maps to a users table which contains user credentials."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        """Show error message when a user tries to edit the password field."""
        raise AttributeError('password is a write-only field')

    @password.setter
    def password(self, password):
        """Create a hashed password."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Compare password_hashes with that saved in the table for user."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Enable printing of the user's username."""
        return "<User: %r>" % self.username


class Bucketlist(db.Model):
    """Maps bucketlists table which contains bucketlist inforamtion."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.now)

    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User",
                           backref=db.backref("user", lazy="dynamic"))

    items = db.relationship("Item",
                            backref=db.backref("bucketlist"))

    def __repr__(self):
        """Enable printing of the Bucketlist title ."""
        return "<Bucketlist: %r>" % self.title


class Item(db.Model):
    """Maps to the items table which contains bucketlist item information."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime,
                              onupdate=datetime.now)
    done = db.Column(db.Boolean, default=False)

    created_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User",
                           backref=db.backref("item", lazy="dynamic"))

    bucketlist_id = db.Column(db.Integer, db.ForeignKey("bucketlist.id"))

    def __repr__(self):
        """Enable printing of the Bucketlist Item name ."""
        return "<Item: %r>" % self.name
