"""Module to run the API."""

from bucketlist.user_routes import Home, UserLogin, UserRegister
from bucketlist.bucketlist_routes import (CreateBucketList, GetAllBucketLists,
                                          GetSingleBucketList)
from bucketlist.item_routes import CreateItem
from bucketlist.app import api, app

# Create api endpoints
api.add_resource(Home, "/")
api.add_resource(UserLogin, "/auth/login/")
api.add_resource(UserRegister, "/auth/register/")
api.add_resource(CreateBucketList, "/bucketlists/")
api.add_resource(GetAllBucketLists, "/bucketlists/")
api.add_resource(GetSingleBucketList, "/bucketlists/<id>")
api.add_resource(CreateItem, "/bucketlists/<id>/items/")




if __name__ == "__main__":
    app.run()
