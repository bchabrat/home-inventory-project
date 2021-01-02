from flask_restful import Api, reqparse, Resource, abort
from model.models import *
from . import auth


room_parser = reqparse.RequestParser()
room_parser.add_argument('name', type=str, help='name of the room')
room_parser.add_argument('new_name', type=str, help='new name of the room')
room_parser.add_argument('id', type=int)

room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)


def room_name_exists(room_name):
    names = [item.name for item in db.session.query(Room).filter_by(user_id=g.user.id).all()]
    if room_name in names:
        return True
    return False

def room_id_exists(id):
    ids = [room.id for room in db.session.query(Room).filter_by(user_id=g.user.id).all()]
    if id in ids:
        return True
    return False


# get a list of all the rooms
class AllRoomResource(Resource):
    @auth.login_required
    def get(self):
        result = db.session.query(Room).filter_by(user_id = g.user.id).all()
        return rooms_schema.dump(result)


# create, read, update and delete a room
class RoomResource(Resource):
    @auth.login_required
    def post(self):
        args = room_parser.parse_args()
        if room_name_exists(args['name']):
            abort(403, message="the name {} already exists".format(args['name']))
        room_to_add = Room(name=args['name'], user_id=g.user.id)
        db.session.add(room_to_add)
        db.session.commit()
        return 201

    @auth.login_required
    def get(self):
        args = room_parser.parse_args()
        if not room_name_exists(args['name']):
            abort(403, message="the room {} you are trying to get does not exists".format(args['name']))
        result = db.session.query(Room.name).filter_by(id=args['id']).one()
        return room_schema.dump(result)

    @auth.login_required
    def put(self):
        args = room_parser.parse_args()
        if not room_id_exists(args['id']):
            abort(403, message="the room {} you are trying to update does not exists".format(args['name']))
        if room_name_exists(args['new_name']):
            abort(403, message="the name {} already exists".format(args['name']))
        room_to_update = db.session.query(Room).get(args['id'])
        room_to_update.name = args['new_name']
        db.session.add(room_to_update)
        db.session.commit()

    @auth.login_required
    def delete(self):
        args = room_parser.parse_args()
        if not room_id_exists(args['id']):
            abort(403, message="the room {} you are trying to delete does not exists".format(args['name']))
        room_to_delete = db.session.query(Room).get(args['id'])
        db.session.delete(room_to_delete)
        db.session.commit()
        return 200