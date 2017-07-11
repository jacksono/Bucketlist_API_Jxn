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

    def post(self):  # noqa
        """
           End point for creating a bucketlist
           ---
           parameters:
             - in: path
               name: title
               type: string
               description: The bucketlist title
               required: true
             - in: path
               name: description
               description: Description of the bucketlist
               type: string
               required: true
           responses:
             201:
               description: Creates a new bucketlist
               schema:
                 id: CreateBucketlist
                 properties:
                   title:
                     type: string
                     default: Travel
                   Description:
                     type: string
                     description: Places to visit
                     default: Hawaii
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

    def get(self):  # noqa
        """
           End point for returning all bucketlists created by the user
           ---
           responses:
             200:
               description: Returns all bucketlists created by the user.
            """
        args = request.args.to_dict()
        page = int(args.get("page", 1))
        try:
            int(args.get("limit", 20))
        except:
            return {"message": "Error! Limit must be an integer"}
        limit = int(args.get("limit", 20))
        if limit < 1:
            return {"message": "Error! Limit must be greater than 0"}
        search_by_name = args.get("q")
        output = {}
        if search_by_name:
            bucketlists = Bucketlist.query.filter_by(
                created_by=g.user.id)
            for num, bucket in enumerate(bucketlists):
                bucket.user_num = num + 1
            results = bucketlists.filter(func.lower(
                Bucketlist.title).contains(search_by_name.lower()))
            bucketlist_pages = results.filter_by(
                created_by=g.user.id).paginate(
                page=page, per_page=limit, error_out=False)
        else:
            bucketlists = Bucketlist.query.filter_by(
                created_by=g.user.id)
            for num, bucket in enumerate(bucketlists):
                bucket.user_num = num + 1
            bucketlist_pages = bucketlists.paginate(
                page=page, per_page=limit, error_out=False)
        no_of_pages = bucketlist_pages.pages
        has_next = bucketlist_pages.has_next
        has_previous = bucketlist_pages.has_prev
        if has_next:
            next_page = (str(request.url_root) + "api/v1/bucketlists?" +
                         "limit=" + str(limit) + "&page=" + str(page + 1))
            output['Next Page'] = next_page
        if has_previous:
            previous_page = (request.url_root + "api/v1/bucketlists?" +
                             "limit=" + str(limit) + "&page=" + str(page - 1))
            output['Previous Page'] = previous_page
        list_of_bucketlists = []
        bucketlists = bucketlist_pages.items
        if bucketlists:
            for num, bucketlist in enumerate(bucketlists):
                result = {}
                items_dict = {}
                items_list = []
                items = Item.query.filter_by(bucketlist_id=bucketlist.id).all()
                if items:
                    item_id = 1
                    for item in items:
                        items_dict["id"] = item_id
                        items_dict["name"] = item.name
                        items_dict["date_created"] = str(item.date_created)
                        items_dict["done"] = str(item.done)
                        items_list.append(items_dict)
                        items_dict = {}
                        item_id += 1
                else:
                    items_list.append({"message": "No items yet"})
                result["id"] = bucketlist.user_num
                result["name"] = bucketlist.title
                result["description"] = bucketlist.description
                result["items"] = items_list
                result["date_created"] = str(bucketlist.date_created)
                result["created_by"] = bucketlist.created_by
                list_of_bucketlists.append(result)
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

    def get(self, id):  # noqa
        """
           End point for returning a single bucketlist
           ---
           parameters:
             - in: path
               name: id
               type: int
               description: The bucketlist id
               required: true
           responses:
             200:
               description: Returns a single bucketlist
               schema:
                 id: GetSingleBucketlist
                 properties:
                   id:
                     type: int
                     default: 1
            """
        if get_bucketlist_by_id(id):
            return get_one_bucketlist(id)
        else:
            return {"message": "That bucketlist does not exist"}, 404


class UpdateBucketList(Resource):
    """Update a bucket list: Route: PUT /bucketlists/<id>."""

    def put(self, id):  # noqa
        """
           End point for editing a bucketlist
           ---
           parameters:
             - in: path
               name: id
               type: int
               description: The bucketlist id
               required: true
             - in: path
               name: title
               type: string
               description: New bucketlist title
               required: true
             - in: path
               name: description
               description: New bucketlist description
               type: string
               required: true
           responses:
             200:
               description: Edits a bucketlist
               schema:
                 id: EditBucketlist
                 properties:
                   title:
                     type: string
                     default: Read
                   description:
                     type: string
                     default: Read through the Bible
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

    def delete(self, id):  # noqa
        """
           End point for deleting a bucketlist
           ---
           parameters:
             - in: path
               name: id
               type: int
               description: The bucketlist id
               required: true
           responses:
             200:
               description: Deletes a bucketlist
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
