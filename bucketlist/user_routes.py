"""Module to define endpoint contents."""
from flask_restful import Resource, reqparse, marshal
from flask import g
from validate_email import validate_email
from bucketlist.models import User
from bucketlist.app import db
from bucketlist.helper_functions import add_user, user_serializer


class Home(Resource):
    """Response to the index route using the GET method."""

    def get(self):
        """Define the home/index url.

        ---
           responses:
             200:
               description: The index url

        """
        return {"message": "This is the Bucketlist API, You are WELCOME!!. "
                "To use the API please register or login"}


class UserRegister(Resource):
    """Register a new user to the route /api/v1/auth/register using POST."""

    def post(self):
        """Create a new user.

        ---
           responses:
             201:
               description: Creates a new user

        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Please enter a username.")
        parser.add_argument(
            "email",
            required=True,
            help="Please enter an email address.")
        parser.add_argument(
            "password",
            required=True,
            help="Please enter a password.")
        args = parser.parse_args()
        username, email, password = (args["username"], args["email"],
                                     args["password"])
        if len(password) < 6:
            return {"message": "ERROR!, Password must be at"
                    " least 6 characters"}, 400
        if validate_email(email, check_mx=True):
            if username.isalnum():
                user = User(username=username, email=email, password=password)
                return add_user(user)
            else:
                return {"message": "ERROR!, Username cannot contain"
                        " special characters or spaces."
                        " Please check and try again"}, 400
        else:
            return {"message": "ERROR!, Invalid email."
                    " Please check and try again"}, 400


class UserLogin(Resource):
    """Log in a user to the route /api/v1/auth/login using POST."""

    def post(self):
        """Login a user.

        ---
           responses:
             200:
               description: Logs in a user

        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "email",
            required=True,
            help="Please enter an email address.")
        parser.add_argument(
            "password",
            required=True,
            help="Please enter a password.")
        args = parser.parse_args()
        email, password = args["email"], args["password"]
        user = User.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                token = user.generate_token()
                return {"message": "Logged in successfully. Your token for"
                        " making requests has been generated",
                        "token": token.decode("ascii")}
            else:
                return {"message": "Error: Incorrect password."
                        " Please check and try again! "}, 400
        else:
            return {"message": "Error: That email is not yet registered."}, 404


class ChangeUsername(Resource):
    """Change user's name: Route: PUT /auth/name."""

    def put(self):
        """Change a user's name.

        ---
           responses:
             200:
               description: Changes a user's name

        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "username",
            required=True,
            help="Please enter a new username.")
        args = parser.parse_args()
        username = args["username"]
        user = User.query.filter_by(email=g.user.email).first()
        if user.username == username:
            return {"message": "Error! Use a new username"}, 400
        user.username = username
        db.session.add(user)
        db.session.commit()

        message = {"message": "Username changed succesfully"}
        message.update(marshal(user, user_serializer))
        return message
