"""Contain helper functions."""

from sqlalchemy.exc import IntegrityError
from bucketlist.app import db, app
from flask import g, request, jsonify
from bucketlist.models import User, Bucketlist, Item
from flask_restful import marshal, fields


@app.before_request
def before_request():
    """Set global attributes."""
    if request.endpoint not in ["userlogin", "userregister", "home"]:
        if request.endpoint in ["createitem",
                                "updateitem",
                                "deleteitem",
                                "createbucketlist",
                                "getallbucketlists",
                                "getsinglebucketlist",
                                "updatebucketlist",
                                "deletebucketlist"]:
            token = request.headers.get("token")
            if token is not None:
                user = User.verify_auth_token(token)
                if user:
                    g.user = user
                else:
                    return jsonify({"message": "Error: Invalid Token"}), 401
            else:
                return jsonify({"message": "Error: Please enter a token"}), 401
        else:
            return jsonify({"message": "Error: Wrong URL or Incorrect request"
                            " METHOD. Please check and try again"}), 400


def add_user(user_object):
    """Add a user, bucket list, or bucket list item to the database."""
    try:
        db.session.add(user_object)
        db.session.commit()
        user_serializer = {"id": fields.Integer,
                           "username": fields.String,
                           "email": fields.String}

        message = {"message": "You have successfully registered."
                   "Please login to get an access token"}
        message.update(marshal(user_object, user_serializer))
        return message, 201

    except IntegrityError:
        """Show when the username already exists"""
        db.session.rollback()
        return {"message": "Error: " + user_object.email +
                " already exists."}, 400


def add_bucketlist(bucketlist_object):
    """Add a bucketlist item to the database."""
    try:
        db.session.add(bucketlist_object)
        db.session.commit()
        bucketlist_serializer = {"id": fields.Integer,
                                 "title": fields.String,
                                 "description": fields.String,
                                 "created_by": fields.Integer,
                                 "date_created": fields.DateTime,
                                 "date_modified": fields.DateTime}
        message = {"message": "You have successfully added a new bucketlist."}
        no_of_user_bucketlists = len(Bucketlist.query.filter_by(
                                    created_by=g.user.id).all())
        bucketlist_object.id = no_of_user_bucketlists
        message.update(marshal(bucketlist_object, bucketlist_serializer))
        return message, 201

    except IntegrityError:
        """Show when the bucketlist already exists"""
        db.session.rollback()
        return {"message": "Error: " + bucketlist_object.title +
                " already exists."}, 400


def add_item(item_object, bucketlist_id, id):
    """Add an item to the bucketlist in the database."""
    try:
        db.session.add(item_object)
        db.session.commit()
        item_serializer = {"id": fields.Integer,
                           "name": fields.String,
                           "done": fields.Boolean,
                           "date_created": fields.DateTime,
                           "date_modified": fields.DateTime,
                           "bucketlist_id": fields.Integer}
        message = {"message": "Item created successfully."}
        no_of_bucketlist_items = len(Item.query.filter_by(
            bucketlist_id=bucketlist_id).all())
        item_object.id = no_of_bucketlist_items
        item_object.bucketlist_id = id
        message.update(marshal(item_object, item_serializer))
        return message, 201

    except IntegrityError:
        """Show when the item already exists"""
        db.session.rollback()
        return {"message": "Error: " + item_object.name +
                " already exists."}, 400
