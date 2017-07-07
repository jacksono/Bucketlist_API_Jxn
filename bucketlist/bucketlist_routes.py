"""Module to define buckeltist endpoints."""

from flask_restful import Resource, reqparse, marshal
from bucketlist.models import Bucketlist, Item
from bucketlist.helper_functions import (add_bucketlist,
                                         bucketlist_serializer)
from flask import g, request
from bucketlist.app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func


def get_bucketlist_by_id(id):
    """Get the a bucket list id as indexed for the current user."""
    bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
    if bucketlists:
        if int(id) > 0 and int(id) <= len(bucketlists):
            bucketlist = bucketlists[int(id) - 1]
            return bucketlist
        else:
            return None
    else:
        return None


def get_one_bucketlist(id):
    """Is a helper function to get a single bucketlist."""
    message = {}
    items_dict = {}
    items_list = []
    bucketlist_id = get_bucketlist_by_id(id).id
    items = Item.query.filter_by(bucketlist_id=bucketlist_id).all()
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
    bucketlist = get_bucketlist_by_id(id)
    if bucketlist:
        message["id"] = int(id)
        message["name"] = bucketlist.title
        message["description"] = bucketlist.description
        message["items"] = items_list
        message["date_created"] = str(bucketlist.date_created)
        message["date_modified"] = str(bucketlist.date_modified)
        message["created_by"] = bucketlist.created_by
        return message


class CreateBucketList(Resource):
    """Create a new bucketlist to the route /api/v1/auth/bucketlists/ using POST.""" # noqa

    def post(self):
        """Create a new bucketlist.

        ---
           responses:
             201:
               description: Creates a new bucketlist

        """
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
        if title and description:
            bucketlist = Bucketlist(title=title,
                                    description=description,
                                    created_by=g.user.id)
            return add_bucketlist(bucketlist)
        else:
            return {"message": "ERROR! Title and/or"
                    " Description can not be empty"}, 400


class GetAllBucketLists(Resource):
    """Shows all bucketlists. Route: /api/v1/auth/bucketlists/ using GET."""

    def get(self):
        """Show all bucketlists.

        ---
           responses:
             200:
               description: Shows all bucketlists

        """
        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        search_by_name = args.get("q")
        output = {}
        if search_by_name:
            results = Bucketlist.query.filter(func.lower(
                Bucketlist.title).contains(search_by_name.lower()))
            bucketlists = results.filter_by(
                created_by=g.user.id).paginate(
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
            output['Next Page'] = next_page
        if has_previous:
            previous_page = (request.url_root + "api/v1/bucketlists?" +
                             "limit=" + str(limit) + "&page=" + str(page - 1))
            output['Previous Page'] = previous_page
        list_of_bucketlists = []
        bucketlists = bucketlists.items
        if bucketlists:
            for number in range(len(bucketlists)):
                list_of_bucketlists.append(get_one_bucketlist(number + 1))
            output.update({"Bucketlists": list_of_bucketlists,
                           "Current Page": page,
                           "No. of pages": no_of_pages,
                           "No. of bucketlists on page": len(
                               list_of_bucketlists)
                           })

            return output
        else:
            return {"message": "No bucketlist by {} matching that"
                    " request".format(g.user.email)}, 404


class GetSingleBucketList(Resource):
    """Get a single bucketlist. Route /bucketlist/<id>."""

    def get(self, id):
        """Show one bucketlist.

        ---
           responses:
             200:
               description: Shows one bucketlist

        """
        if get_bucketlist_by_id(id):
            return get_one_bucketlist(id)
        else:
            return {"message": "That bucketlist does not exist"}, 404


class UpdateBucketList(Resource):
    """Update a bucket list: Route: PUT /bucketlists/<id>."""

    def put(self, id):
        """Update one bucketlist.

        ---
           responses:
             200:
               description: Updates one bucketlist

        """
        if not get_bucketlist_by_id(id):
            return {"message": "ERROR! Cannot update a"
                    " bucketlsit that doesnot exist"}, 404
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
        bucketlist = get_bucketlist_by_id(id)
        if bucketlist.title == title or\
           bucketlist.description == description:
            return {"message": "ERROR: Please use a new Title"
                    " and Description"}, 400

        else:
            bucketlist.title = title
            bucketlist.description = description
            bucketlist.date_modified = datetime.now()
        try:
            db.session.add(bucketlist)
            db.session.commit()
        except IntegrityError:
            """Show when the the title already exists"""
            db.session.rollback()
            return {"message": "Error: Bucketlist with title " + title +
                    " already exists."}, 400
        message = {"message": "Bucket list updated succesfully"}
        bucketlist.id = id
        message.update(marshal(bucketlist, bucketlist_serializer))
        return message


class DeleteBucketList(Resource):
    """Delete a single bucketlist. Route: DELETE /bucketlists/<id>."""

    def delete(self, id):
        """Delete one bucketlist.

        ---
           responses:
             200:
               description: Deletes one bucketlist

        """
        bucketlist = get_bucketlist_by_id(id)
        if bucketlist:
            items = Item.query.filter_by(bucketlist_id=id).all()
            if items:
                for item in items:
                    db.session.delete(item)
            db.session.delete(bucketlist)
            db.session.commit()
            return {"message": "Bucketlist deleted successfully"}
        else:
            return {"message": "ERROR! Cannot delete a"
                    " bucketlsit that does not exist"}, 404
