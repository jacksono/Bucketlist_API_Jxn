"""Module to define items endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Item
from bucketlist.helper_functions import add_item
from bucketlist.app import db


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
