"""Module to define items endpoints."""

from flask_restful import Resource, reqparse, marshal
from bucketlist.models import Item
from bucketlist.helper_functions import add_item, item_serializer
from bucketlist.bucketlist_routes import get_bucketlist_by_id
from bucketlist.app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError


def get_item_by_id(bucketlist_id, item_id):
    """Get an item as indexed for the current user."""
    items = Item.query.filter_by(bucketlist_id=bucketlist_id).all()
    if items:
        if int(item_id) > 0 and int(item_id) <= len(items):
            item = items[int(item_id) - 1]
            return item
        else:
            return None
    else:
        return None


class CreateItem(Resource):
    """Create a new bucketlist item. Route: /bucketlists/<id>/items/."""

    def post(self, id):
        """Create a new bucketlist item.

        ---
           responses:
             201:
               description: Creates a new bucketlist item

        """
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            required=True,
            help="Please enter a bucketlist item name.")
        parser.add_argument(
                            "done",
                            required=True,
                            help="Please enter the  status")
        args = parser.parse_args()
        name, done = args["name"], args["done"]
        if name and done:
            if done.lower() == 'y':
                done = True
            elif done.lower() == 'n':
                done = False
            else:
                return {'message': "Please use Y/N or y/n for status"}
            bucketlist_id = get_bucketlist_by_id(id).id
            item = Item(name=name, done=done, bucketlist_id=bucketlist_id)
            return add_item(item, bucketlist_id, id)
        else:
            return {"message": "ERROR! Name and/or"
                    " Status can not be empty"}, 400


class DeleteItem(Resource):
    """Delete bucketlist item. Route: /bucketlists/<id>/items/<item_id>."""

    def delete(self, id, item_id):
        """Delete one bucketlist item.

        ---
           responses:
             200:
               description: Deletes one bucketlist item

        """
        if get_bucketlist_by_id(id):
            bucketlist_id = get_bucketlist_by_id(id).id
        else:
            return {"message": "ERROR!: That Bucketlist does not exists"}, 404
        items = Item.query.filter_by(bucketlist_id=bucketlist_id).all()
        if items:
            if int(item_id) <= len(items):
                item = items[int(item_id) - 1]
                db.session.delete(item)
                db.session.commit()
                return {"message": "Item deleted succesfully"}
            else:
                return {"message": "That item doesnot exist"}, 404
        else:
            return {"message": "ERROR!: That Bucketlist does not "
                    " have any items"}, 404


class UpdateItem(Resource):
    """Update a bucketlist item.Route: /bucketlists/<id>/items/<item_id>."""

    def put(self, id, item_id):
        """Update one bucketlist item.

        ---
           responses:
             200:
               description: Update one bucketlist item

        """
        if get_bucketlist_by_id(id):
            bucketlist_id = get_bucketlist_by_id(id).id
        else:
            return {"message": "That bucketlist does not exist"}, 404
        items = Item.query.filter_by(bucketlist_id=bucketlist_id).all()
        if items:
            if int(item_id) <= len(items):
                parser = reqparse.RequestParser()
                parser.add_argument(
                    "name",
                    required=True,
                    help="Please enter new item name.")
                parser.add_argument(
                                    "done",
                                    required=True,
                                    help="Please enter item status")
                args = parser.parse_args()
                name, done = args["name"], args["done"]
                if done.lower() == 'y':
                    done = True
                elif done.lower() == 'n':
                    done = False
                else:
                    return {'message': "Please use Y/N or y/n for status"}
                item_to_update = items[int(item_id) - 1]
                if name == item_to_update.name:
                    return {'message': "ERROR! Use a new name"}
                item_to_update.name = name
                item_to_update.done = done
                item_to_update.date_modified = datetime.now()
                db.session.add(item_to_update)
                try:
                    db.session.commit()
                except IntegrityError:
                    """Show when the item already exists"""
                    db.session.rollback()
                    return {"message": "Error: " + item_to_update.name +
                            " already exists."}, 400
                message = {"message": "Item updated succesfully"}
                item_to_update.id = item_id
                item_to_update.bucketlist_id = id
                message.update(marshal(item_to_update, item_serializer))
                return message
            else:
                return {"message": "Item does not exist inthe bucketlist"}, 404
        else:
            return {"message": "That bucketlist has no items"}, 404


class GetAllItems(Resource):
    """Shhow all bucketlist items.Route: /bucketlists/<id>/items/."""

    def get(self, id):
        """Get all bucketlist items.

        ---
           responses:
             200:
               description: Gets all bucketlist items

        """
        if get_bucketlist_by_id(id):
            bucketlist_id = get_bucketlist_by_id(id).id
        else:
            return {"message": "That bucketlist does not exist"}, 404
        items = Item.query.filter_by(bucketlist_id=bucketlist_id).all()
        items_dict = {}
        items_list = []
        if items:
            item_id = 1
            for item in items:
                items_dict["id"] = item_id
                items_dict["name"] = item.name
                items_dict["date_modified"] = str(item.date_modified)
                items_dict["date_created"] = str(item.date_created)
                items_dict["done"] = str(item.done)
                items_list.append(items_dict)
                items_dict = {}
                item_id += 1
            return {"items": items_list}
        else:
            return {"message": "No items yet"}
