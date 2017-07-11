"""Module to define endpoint contents."""
from flask_restful import Resource, reqparse, marshal
from flask import g
from validate_email import validate_email
from bucketlist.models import User
from bucketlist.app import db
from bucketlist.helper_functions import add_user, user_serializer


class Home(Resource):
    """Response to the index route using the GET method."""

    def get(self):  # noqa
        """
           This is the index page with a welcome message
           ---
           parameters:
             - in: path
           responses:
             200:
               description: A simple welcome message is returned
            """
        return {"message": "This is the Bucketlist API, You are WELCOME!!. "
                "To use the API please register or login"}


class UserRegister(Resource):
    """Register a new user to the route /api/v1/auth/register using POST."""

    def post(self):  # noqa
        """
           This is the register end point for creating a user account
           ---
           parameters:
             - in: path
               name: email
               type: string
               description: The email of the to be registered
               required: true
             - in: path
               name: username
               description: The name of the user to be created
               type: string
               required: true
             - in: path
               name: password
               type: string
               description: The password of the user
               required: true
           responses:
             201:
               description: Create a user account
               schema:
                 id: Register
                 properties:
                   username:
                     type: string
                     description: The name of the user to be created
                     default: user
                   email:
                     type: string
                     description: The email of the to be registered
                     default: user@email.com
                   password:
                     type: string
                     description: The password of the user
                     default: passw0rD
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

    def post(self):  # noqa
        """
           This is the login end point for logging in a user
           ---
           parameters:
             - in: path
               name: email
               type: string
               description: The email address of the user
               required: true
             - in: path
               name: password
               type: string
               description: The password of the user
               required: true
           responses:
             200:
               description: Logs in a user
               schema:
                 id: Login
                 properties:
                   email:
                     type: string
                     default: user@email.com
                   password:
                     type: string
                     default: passw0rD
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

    def put(self):  # noqa
        """
           End point for a user to change their username
           ---
           parameters:
             - in: path
               name: username
               type: string
               description: The user's username
               required: true
           responses:
             200:
               description: Changes a user's username
               schema:
                 id: ChangeName
                 properties:
                   username:
                     type: string
                     default: user
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
