"""Module to define items endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Item
from bucketlist.helper_functions import add_item


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
