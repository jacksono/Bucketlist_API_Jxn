"""Contain helper functions."""

from sqlalchemy.exc import IntegrityError
from bucketlist.app import db
from flask_restful import marshal
from flask_restful import fields
from bucketlist.app import app
from flask import g, request
from bucketlist.models import User, Bucketlist


@app.before_request
def before_request():
    """Set global attributes."""
    if request.endpoint not in ["userlogin", "userregister", "home"]:
        if request.headers.get("username"):
            username = request.headers.get("username")
            user = User.query.filter_by(username=username).first()
            if user:
                g.user = user
    if request.headers.get("bucketlist"):
        bucketlist_name = request.headers.get("bucketlist")
        bucketlist = Bucketlist.query.filter_by(title=bucketlist_name).first()
        if bucketlist:
            g.bucketlist = bucketlist


def add_user(user_object):
    """Add a user, bucket list, or bucket list item to the database."""
    try:
        db.session.add(user_object)
        db.session.commit()

        message = {"message": "You have successfully added a new user "}
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


def add_bucketlist(bucketlist_object):
    """Add a bucketlist item to the database."""
    try:
        db.session.add(bucketlist_object)
        db.session.commit()
        message = {"message": "You have successfully added a new bucketlist."}
        bucketlist_serializer = {
                                "id": fields.Integer,
                                "title": fields.String,
                                "description": fields.String,
                                "created_by": fields.Integer,
                                "date_created": fields.DateTime,
                                "date_modified": fields.DateTime
                                }
        response = marshal(bucketlist_object, bucketlist_serializer)
        response.update(message)
        return response, 201

    except IntegrityError:
        """Show when the bucketlist already exists"""
        db.session.rollback()
        return {"message": "Error: " + bucketlist_object.title +
                " already exists."}


def add_item(item_object):
    """Add an item to the bucketlist in the database."""
    try:
        db.session.add(item_object)
        db.session.commit()
        message = {"message": "Item created successfully."}
        item_serializer = {
                                "id": fields.Integer,
                                "name": fields.String,
                                "bucketlist_id": fields.Integer,
                                "date_created": fields.DateTime,
                                "date_modified": fields.DateTime,
                                "done": fields.String
                                }
        response = marshal(item_object, item_serializer)
        response.update(message)
        return response, 201

    except IntegrityError:
        """Show when the item already exists"""
        db.session.rollback()
        return {"message": "Error: " + item_object.name +
                " already exists."}
