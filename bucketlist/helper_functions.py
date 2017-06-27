"""Contain helper functions."""

from sqlalchemy.exc import IntegrityError
from bucketlist.app import db, app
from flask import g, request, jsonify
from bucketlist.models import User


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

        message = {"message": "You have successfully registered."
                   "Please login to get an access token"}
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
        message = {"message": "You have successfully added a new bucketlist."}
        return message, 201

    except IntegrityError:
        """Show when the bucketlist already exists"""
        db.session.rollback()
        return {"message": "Error: " + bucketlist_object.title +
                " already exists."}, 400


def add_item(item_object):
    """Add an item to the bucketlist in the database."""
    try:
        db.session.add(item_object)
        db.session.commit()
        message = {"message": "Item created successfully."}
        return message, 201

    except IntegrityError:
        """Show when the item already exists"""
        db.session.rollback()
        return {"message": "Error: " + item_object.name +
                " already exists."}, 400
