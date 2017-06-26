"""Module to define buckeltist endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Bucketlist, Item
from bucketlist.helper_functions import (add_bucketlist)
from flask import g, request
from bucketlist.app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def get_bucketlist(id):
    """Is a helper function to get a single bucketlist."""
    message = {}
    items_dict = {}
    items_list = []
    items = Item.query.filter_by(bucketlist_id=id).all()
    if items:
        item_id = 1
        for item in items:
            items_dict["id"] = item_id
            items_dict["name"] = item.name
            items_dict["date_modified"] = str(item.date_modified)
            items_dict["date_created"] = str(item.date_created)
            items_dict["done"] = str(item.done)
            items_list.append(items_dict)
            items_dict = {}
            item_id += 1
    else:
        items_list.append({"message": "No items yet"})
    bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
    if bucketlists:
        if int(id) <= len(bucketlists):
            bucketlist = bucketlists[int(id) - 1]
            message["id"] = int(id)
            message["name"] = bucketlist.title
            message["description"] = bucketlist.description
            message["items"] = items_list
            message["date_created"] = str(bucketlist.date_created)
            message["date_modified"] = str(bucketlist.date_modified)
            message["created_by"] = bucketlist.created_by
            return message
        else:
            return {"message": "That bucketlist does not exist"}
    else:
        return {"message": "You have no bucketlists yet"}


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
        """Show all bucketlists and implements pagination and searching by name.

        Route: /api/v1/auth/bucketlists/ using GET.
        """
        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        search_by_name = args.get("q")
        if search_by_name:
            bucketlists = Bucketlist.query.filter_by(
                created_by=g.user.id, title=search_by_name).paginate(
                page=page, per_page=limit, error_out=False)
        else:
            bucketlists = Bucketlist.query.filter_by(
                created_by=g.user.id).paginate(
                page=page, per_page=limit, error_out=False)
        no_of_pages = bucketlists.pages
        has_next = bucketlists.has_next
        has_previous = bucketlists.has_prev
        if has_next:
            next_page = (str(request.url_root) + "api/v1/bucketlists?" +
                         "limit=" + str(limit) + "&page=" + str(page + 1))
        else:
            next_page = "None"
        if has_previous:
            previous_page = (request.url_root + "api/v1/bucketlists?" +
                             "limit=" + str(limit) + "&page=" + str(page - 1))
        else:
            previous_page = "None"
        list_of_bucketlists = []
        bucketlists = bucketlists.items
        for number in range(len(bucketlists)):
            list_of_bucketlists.append(get_bucketlist(number + 1))

        output = {"Bucketlists": list_of_bucketlists,
                  "Current Page": page,
                  "No. of pages": no_of_pages,
                  "Previous page": previous_page,
                  "Next page": next_page,
                  "No. of bucketlists on page": len(list_of_bucketlists)
                  }

        if bucketlists:
            return output
        else:
            return {"message": "No bucketlist by {} matching that"
                    " request".format(g.user.username)}


class GetSingleBucketList(Resource):
    """Get a single bucketlist. Route /bucketlist/<id>."""

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
            help="Please enter a new bucketlist title.")
        parser.add_argument(
                            "description",
                            required=True,
                            help="Please enter a new description")
        args = parser.parse_args()
        title, description = args["title"], args["description"]
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        bucketlist.title = title
        bucketlist.description = description
        bucketlist.date_modified = datetime.now()
        try:
            db.session.add(bucketlist)
            db.session.commit()
        except IntegrityError:
            """Show when the username already exists"""
            db.session.rollback()
            return {"message": "Error: " + title +
                    " already exists."}
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
            return {"message": "That bucketlist does not exist"}
