from flask_restful import Api, reqparse, Resource, abort
from model.models import *


item_parser = reqparse.RequestParser()
item_parser.add_argument('name', type=str, help='name of the item')
item_parser.add_argument('room_name', type=str, help='name of the room where the item is located')
item_parser.add_argument('container_name', type=str, help='name of the container where the item is located')
item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


def item_name_exits(item_name):
    names = [item.name for item in db.session.query(Item).all()]
    if item_name in names:
        result = True
    else:
        result = False
    return result


# get a list of all the items
class AllItemResource(Resource):
    def get(self):
        result = db.session.query(Item).all()
        return items_schema.dump(result)


# create, read, update and delete an item
class ItemResource(Resource):
    def post(self, item_name):
        if item_name_exits(item_name):
            abort(403, message="the name {} already exists".format(item_name))
        args = item_parser.parse_args()
        item_to_add = Item(name=item_name, room_name=args['room_name'], container_name=args['container_name'])
        db.session.add(item_to_add)
        db.session.commit()
        return 201

    def get(self, item_name):
        if not item_name_exits(item_name):
            abort(403, message="the item {} you are trying to get does not exists".format(item_name))
        result = db.session.query(Item).filter_by(name=item_name).one()
        return item_schema.dump(result)

    def put(self, item_name):
        if not item_name_exits(item_name):
            abort(403, message="the item {} you are trying to update does not exists".format(item_name))
        args = item_parser.parse_args()
        if item_name_exits(args['name']):
            abort(403, message="the name {} already exists".format(args['name']))
        item_to_update = db.session.query(Item).get(item_name)
        if args['name'] is not None:
            item_to_update.name = args['name']
        if args['container_name'] is not None:
            item_to_update.container_name = args['container_name']
        if args['room_name'] is not None:
            item_to_update.room_name = args['room_name']
        db.session.add(item_to_update)
        db.session.commit()

    def delete(self, item_name):
        if not item_name_exits(item_name):
            abort(403, message="the container {} you are trying to delete does not exists".format(item_name))
        item_to_delete = db.session.query(Item).get(item_name)
        db.session.delete(item_to_delete)
        db.session.commit()
        return 200
