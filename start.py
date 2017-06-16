"""Module to run the API."""

from bucketlist.user_routes import Home
from bucketlist.app import api, app

# Create api endpoints
api.add_resource(Home, "/")


if __name__ == "__main__":
    app.run()
