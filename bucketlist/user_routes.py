"""Module to define endpoint contents."""
from flask_restful import Resource
from flask_restful import reqparse
from bucketlist.models import User


class Home(Resource):
    """Response to the index route using the GET method"""

    def get(self):
        """Content displayed when index route is accessed."""
        return {"message": "This is the Bucketlist API, You are WELCOME!!. "
                "To use the API please register or login"}


class UserLogin(Resource):
    """Log in a user tot he route /api/v1/auth/login/ using POST."""

    def post(self):
        """Parse data through the header."""
        parser = reqparse.RequestParser()
        parser.add_argument(
                            "username",
                            required=True,
                            help="Enter your username.")
        parser.add_argument(
                            "password",
                            required=True,
                            help="Enter your password.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]

        if username and password:
            user = User.query.filter_by(username=username).first()
        else:
            return {"message": "Error: Please enter a username and password."}
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {"message": "You have successfully logged in. Use the "
                    "token below to make requests.",
                    "token": token.decode("ascii")}
        else:
            return unauthorized("Error: Incorrect username and/or password. "
                                "Please try again!")
