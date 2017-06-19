"""Module to define buckeltist endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Bucketlist, Item
from bucketlist.helper_functions import add_bucketlist
from flask import g
from bucketlist.app import db
from datetime import datetime


def get_bucketlist(id):
    """Get a single bucketlist."""
    message = {}
    items_dict = {}
    items_list = []
    items = Item.query.filter_by(bucketlist_id=id).all()
    if items:
        for item in items:
            items_dict["id"] = item.id
            items_dict["name"] = item.name
            items_dict["date_modified"] = str(item.date_modified)
            items_dict["date_created"] = str(item.date_created)
            items_dict["done"] = str(item.done)
            items_list.append(items_dict)
            items_dict = {}
    else:
        items_list.append({"message": "No items yet"})
    bucketlist = Bucketlist.query.get(id)
    if bucketlist:
        message["id"] = bucketlist.id
        message["name"] = bucketlist.title
        message["description"] = bucketlist.description
        message["items"] = items_list
        message["date_created"] = str(bucketlist.date_created)
        message["date_modified"] = str(bucketlist.date_modified)
        message["created_by"] = bucketlist.created_by
        return message
    else:
        return {"message": "That bucketlist doesnot exist"}


class CreateBucketList(Resource):
    """Create a new bucketlist to the route /api/v1/auth/bucketlists/ using POST.""" # noqa

    def post(self):
        """Create a bucketlist."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "title",
            required=True,
            help="Please enter a bucketlist title.")
        parser.add_argument(
                            "description",
                            required=True,
                            help="Please enter a description")
        args = parser.parse_args()
        title, description = args["title"], args["description"]
        bucketlist = Bucketlist(title=title,
                                description=description,
                                created_by=g.user.id)
        return add_bucketlist(bucketlist)


class GetAllBucketLists(Resource):
    """Shows all bucketlists. Route: /api/v1/auth/bucketlists/ using GET."""

    def get(self):
        """Show all bucketlists.Route: /api/v1/auth/bucketlists/ using GET."""
        output = []
        bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
        if bucketlists:
            for bucketlist in bucketlists:
                output.append(get_bucketlist(id=bucketlist.id))
            return output
        else:
            return {"message": "No bucketlist yet"}


class GetSingleBucketList(Resource):
    """Get a single bucketlist. Route /bucketlist/<id>/."""

    def get(self, id):
        """Get a single bucketlist. Route /bucketlist/<id>/."""
        return get_bucketlist(id)


class UpdateBucketList(Resource):
    """Update a bucket list: Route: PUT /bucketlists/<id>."""

    def put(self, id):
        """Update bucketlist."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "title",
            required=True,
            help="Please enter a bucketlist title.")
        parser.add_argument(
                            "description",
                            required=True,
                            help="Please enter a description")
        args = parser.parse_args()
        title, description = args["title"], args["description"]
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        bucketlist.title = title
        bucketlist.description = description
        bucketlist.date_modified = datetime.now()
        db.session.add(bucketlist)
        db.session.commit()
        return {"message": "Bucket list updated succesfully"}


class DeleteBucketList(Resource):
    """Delete a single bucketlist. Route: DELETE /bucketlists/<id>."""

    def delete(self, id):
        """Delete a bucketlist."""
        bucketlist = Bucketlist.query.get(id)
        if bucketlist:
            items = Item.query.filter_by(bucketlist_id=id).all()
            if items:
                for item in items:
                    db.session.delete(item)
            db.session.delete(bucketlist)
            db.session.commit()
            return {"message": "Bucketlist deleted successfully"}
        else:
            return {"message": "That bucketlist doesnot exist"}
