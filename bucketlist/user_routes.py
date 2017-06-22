"""Module to define endpoint contents."""
from flask_restful import Resource, reqparse
from bucketlist.models import User
from bucketlist.helper_functions import add_user


class Home(Resource):
    """Response to the index route using the GET method."""

    def get(self):
        """Content displayed when index route is accessed."""
        return {"message": "This is the Bucketlist API, You are WELCOME!!. "
                "To use the API please register or login"}


class UserRegister(Resource):
    """Register a new user to the route /api/v1/auth/register using POST."""

    def post(self):
        """Register a user."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Please enter a username.")
        parser.add_argument(
            "password",
            required=True,
            help="Please enter a password.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]
        user = User(username=username,
                    password=password)
        return add_user(user)


class UserLogin(Resource):
    """Log in a user to the route /api/v1/auth/login using POST."""

    def post(self):
        """Parse data through the header."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Please enter a username.")
        parser.add_argument(
            "password",
            required=True,
            help="Please enter a password.")
        args = parser.parse_args()
        username, password = args["username"], args["password"]
        user = User.query.filter_by(username=username).first()
        if user:
            if user.verify_password(password):
                token = user.generate_token()
                return {"message": "Logged in successfully. Your token for"
                        " making requests is below",
                        "token": token.decode("ascii")}
            else:
                return {"message": "Error: Incorrect password."
                        " Please check and try again! "}
        else:
            return {"message": "Error: User not found."
                    " Please check and try again!"}
