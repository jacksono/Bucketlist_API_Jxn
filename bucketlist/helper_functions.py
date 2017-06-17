"""Contain helper functions."""

from sqlalchemy.exc import IntegrityError
from bucketlist.app import db
from flask_restful import marshal
from flask_restful import fields


def add_user(user_object):
    """Add a user, bucket list, or bucket list item to the database."""
    try:
        db.session.add(user_object)
        db.session.commit()

        message = {"message": "You have successfully added a new user."}
        user_serializer = {
                        "id": fields.Integer,
                        "username": fields.String}
        response = marshal(user_object, user_serializer)
        response.update(message)
        return response, 201

    except IntegrityError:
        """Show when the username already exists"""
        db.session.rollback()
        return {"message": "Error: " + user_object.username +
                " already exists."}
