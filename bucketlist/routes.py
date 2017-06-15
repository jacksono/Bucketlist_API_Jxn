"""Module to define endpoint contents."""
from flask_restful import Resource


class Home(Resource):
    """Response to the index route."""

    def get(self):
        """Content displayed when index route is accessed."""
        return {"message": "This is the Bucketlist API, You are WELCOME!!. "
                "To use the API please register or login"}
