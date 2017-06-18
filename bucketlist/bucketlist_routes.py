"""Module to define buckeltist endpoints."""

from flask_restful import Resource, reqparse
from bucketlist.models import Bucketlist
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
        bucketlists = Bucketlist.query.filter_by(created_by=g.user.id).all()
        for bucketlist in bucketlists:
            message["id"] = bucketlist.id
            message["name"] = bucketlist.title
            message["date_created"] = str(bucketlist.date_created)
            message["date_modified"] = str(bucketlist.date_modified)
            message["created_by"] = bucketlist.created_by
            data.append(message)

        return data