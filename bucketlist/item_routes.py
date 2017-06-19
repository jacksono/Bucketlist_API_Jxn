"""Module to define items endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Item
from bucketlist.helper_functions import add_item
from bucketlist.app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError


class CreateItem(Resource):
    """Create a new bucketlist item. Route: /bucketlists/<id>/items/."""

    def post(self, id):
        """Create a new bucketlist item."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            required=True,
            help="Please enter a bucketlist item name.")
        parser.add_argument(
                            "done",
                            required=True,
                            help="Please enter the status")
        args = parser.parse_args()
        name, done = args["name"], args["done"]
        item = Item(name=name, done=done, bucketlist_id=id)
        return add_item(item)


class DeleteItem(Resource):
    """Delete bucketlist item. Route: /bucketlists/<id>/items/<item_id>."""

    def delete(self, id, item_id):
        """Delete bucketlist item."""
        items = Item.query.filter_by(bucketlist_id=id).all()
        if items:
            if int(item_id) <= len(items):
                item = items[int(item_id) - 1]
                db.session.delete(item)
                db.session.commit()
                return {"message": "Item deleted succesfully"}
            else:
                return {"message": "That item doesnot exist"}
        else:
            return {"message": "ERROR!: That Bucketlist does not exists"
                    " or does not have any items"}


class UpdateItem(Resource):
    """Update a bucketlist item.Route: /bucketlists/<id>/items/<item_id>."""

    def put(self, id, item_id):
        """Update a bucketlist item."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            required=True,
            help="Please enter new item name.")
        parser.add_argument(
                            "done",
                            required=True,
                            help="Please enter item status")
        args = parser.parse_args()
        name, done = args["name"], args["done"]
        items = Item.query.filter_by(bucketlist_id=id).all()
        if items:
            if int(item_id) <= len(items):
                item_to_update = items[int(item_id) - 1]
                item_to_update.name = name
                item_to_update.done = done
                item_to_update.date_modified = datetime.now()
                db.session.add(item_to_update)
                try:
                    db.session.commit()
                except IntegrityError:
                    """Show when the item already exists"""
                    db.session.rollback()
                    return {"message": "Error: " + item_to_update.name +
                            " already exists."}
                return {"message": "Item updated succesfully"}
            else:
                return {"message": "Item doesnot exist in the bucketlist"}
        else:
            return {"message": "That bucketlist has no items"}
