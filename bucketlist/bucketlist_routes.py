"""Module to define buckeltist endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Bucketlist, Item
from bucketlist.helper_functions import add_bucketlist
from flask import g


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
        message = {}
        data = []
        items_dict = {}
        items_list = []
        items = Item.query.filter_by(bucketlist_id=g.bucketlist.id).all()
        if items:
            for item in items:
                items_dict["id"] = item.id
                items_dict["name"] = item.name
                items_dict["date_modified"] = str(item.date_modified)
                items_dict["date_created"] = str(item.date_created)
                items_dict["done"] = str(item.done)
                items_list.append(items_dict)
                items_list = []
        else:
            items_list.append({"message": "No items yet"})
        bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
        if bucketlists:
            for bucketlist in bucketlists:
                message["id"] = bucketlist.id
                message["name"] = bucketlist.title
                message["items"] = items_list
                message["date_created"] = str(bucketlist.date_created)
                message["date_modified"] = str(bucketlist.date_modified)
                message["created_by"] = bucketlist.created_by
                data.append(message)
                message = {}
            return data
        else:
            return {"message": "No bucketlist yet"}


class GetSingleBucketList(Resource):
    """Get a single bucketlist. Route /bucketlist/<id>/."""

    def get(self, id):
        """Get a single bucketlist. Route /bucketlist/<id>/."""
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
                items_list = []
        else:
            items_list.append({"message": "No items yet"})
        bucketlist = Bucketlist.query.get(id)
        if bucketlist:
            message["id"] = bucketlist.id
            message["name"] = bucketlist.title
            message["items"] = items_list
            message["date_created"] = str(bucketlist.date_created)
            message["date_modified"] = str(bucketlist.date_modified)
            message["created_by"] = bucketlist.created_by
            return message
        else:
            return {"message": "That bucketlist doesnot exist"}
