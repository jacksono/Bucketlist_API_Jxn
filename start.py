"""Module to run the API."""

from bucketlist.user_routes import (Home,
                                    UserLogin,
                                    UserRegister,
                                    ChangeUsername)
from bucketlist.bucketlist_routes import (CreateBucketList,
                                          GetAllBucketLists,
                                          GetSingleBucketList,
                                          UpdateBucketList,
                                          DeleteBucketList,)
from bucketlist.item_routes import (CreateItem,
                                    UpdateItem,
                                    DeleteItem,
                                    GetAllItems)
from bucketlist.app import api, app


# Create api endpoints
api.add_resource(Home, "/")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(ChangeUsername, "/auth/name")
api.add_resource(CreateBucketList, "/bucketlists/")
api.add_resource(GetAllBucketLists, "/bucketlists/")
api.add_resource(GetSingleBucketList, "/bucketlists/<id>")
api.add_resource(CreateItem, "/bucketlists/<id>/items/")
api.add_resource(UpdateBucketList, "/bucketlists/<id>")
api.add_resource(DeleteBucketList, "/bucketlists/<id>")
api.add_resource(DeleteItem, "/bucketlists/<id>/items/<item_id>")
api.add_resource(UpdateItem, "/bucketlists/<id>/items/<item_id>")
api.add_resource(GetAllItems, "/bucketlists/<id>/items/")


if __name__ == "__main__":
    app.run()
