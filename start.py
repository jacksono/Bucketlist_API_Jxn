"""Module to run the API."""

from bucketlist.user_routes import Home, UserLogin, UserRegister
from bucketlist.app import api, app

# Create api endpoints
api.add_resource(Home, "/")
api.add_resource(UserLogin, "/auth/login/")
api.add_resource(UserRegister, "/auth/register/")


if __name__ == "__main__":
    app.run()
