from flask_restful import Api, reqparse, Resource, abort
from model.models import *
from . import auth


item_parser = reqparse.RequestParser()
item_parser.add_argument('id', type=int)
item_parser.add_argument('name', type=str, help=' name of the item')
item_parser.add_argument('new_name', type=str, help='new name of the item')
item_parser.add_argument('room_id', type=int, help='id of the room where the item is located')
item_parser.add_argument('container_id', type=int, help='id of the container where the item is located')


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


def item_name_exits(item_name):
    names = [item.name for item in db.session.query(Item).filter_by(user_id=g.user.id).all()]
    if item_name in names:
        return True
    return False

def item_id_exists(item_id):
    ids = [item.id for item in db.session.query(Item).filter_by(user_id=g.user.id).all()]
    if item_id in ids:
        return True
    return False


# get a list of all the items
class AllItemResource(Resource):
    @auth.login_required
    def get(self):
        result = db.session.query(Item).filter_by(user_id=g.user.id).join(Items.room).all()
        return items_schema.dump(result)


# create, read, update and delete an item
class ItemResource(Resource):
    @auth.login_required
    def post(self):
        args = item_parser.parse_args()
        if item_name_exits(args['name']):
            abort(403, message="the name {} already exists".format(args['name']))
        item_to_add = Item(name=args['name'], room_id=args['room_id'], container_id=args['container_id'], user_id=g.user.id)
        db.session.add(item_to_add)
        db.session.commit()
        return 201

    @auth.login_required
    def get(self):
        args = item_parser.parse_args()
        if not item_name_exits(args['name']):
            abort(403, message="the item {} you are trying to get does not exists".format(args['name']))
        result = db.session.query(Item).filter_by(name=args['name']).one()
        return item_schema.dump(result)

    @auth.login_required
    def put(self):
        args = item_parser.parse_args()
        if not item_id_exists(args['id']):
            abort(403, message="the item {} you are trying to update does not exists".format(item_name))
        if item_name_exits(args['new_name']):
            abort(403, message="the name {} already exists".format(args['new_name']))
        item_to_update = db.session.query(Item).get(args['id'])
        if args['new_name'] is not None:
            item_to_update.name = args['new_name']
        if args['container_id'] is not None:
            item_to_update.container_id = args['container_id']
        if args['room_id'] is not None:
            item_to_update.room_id = args['room_id']
        db.session.add(item_to_update)
        db.session.commit()

    @auth.login_required
    def delete(self):
        args = item_parser.parse_args()
        if not item_id_exists(args['id']):
            abort(403, message="the container {} you are trying to delete does not exists".format(args['name']))
        item_to_delete = db.session.query(Item).get(args['id'])
        db.session.delete(item_to_delete)
        db.session.commit()
        return 200
