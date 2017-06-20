"""Contain helper functions."""

from sqlalchemy.exc import IntegrityError
from bucketlist.app import db
from flask_restful import marshal
from flask_restful import fields
from bucketlist.app import app
from flask import g, request, jsonify
from bucketlist.models import User, Bucketlist


@app.before_request
def before_request():
    """Set global attributes."""
    if request.endpoint not in ["userlogin", "userregister", "home"]:
        token = request.headers.get("token")
        if token is not None:
            user = User.verify_auth_token(token)
            if user:
                g.user = user
            else:
                return jsonify({"message": "Error: Invalid Token"})
        else:
            return jsonify({"message": "Error: Please enter a token"})


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


def authorized_for_bucketlist(function):
    """Verify if the bucketlist belongs to the current user."""
    def auth_wrapper(*args, **kwargs):
        """Set decorator."""
        g.bucketlist = Bucketlist.query.filter_by(id=kwargs["id"]).first()
        if g.bucketlist:
            if g.bucketlist.created_by == g.user.id:
                return function(*args, **kwargs)
            return jsonify({"message": "Error: Cannot see / modify bucketlist"
                            " created by someonelse"})
        else:
            return jsonify({"message": "That Bucketlist doesnot exist"})
    return auth_wrapper
