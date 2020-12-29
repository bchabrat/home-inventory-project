from flask_restful import Api, reqparse, Resource, abort
from model.models import *

room_post_parser = reqparse.RequestParser()
room_post_parser.add_argument('name', type=str, help='name of the room')
room_schema = RoomSchema()
rooms_schema = RoomSchema(many=True)


def room_name_exists(room_name):
    names = [item.name for item in db.session.query(Room).all()]
    if room_name in names:
        result = True
    else:
        result = False
    return result


def room_id_exists(room_id):
    if room_id in db.session.query(Room):
        result = True
    else:
        result = False
    return result


# get a list of all the rooms
class AllRoomResource(Resource):
    def get(self):
        result = db.session.query(Room).all()
        return rooms_schema.dump(result)


# create, read, update and delete a room
class RoomResource(Resource):
    def post(self, room_name):
        if room_name_exists(room_name):
            abort(403, message="the name {} already exists".format(room_name))
        room_to_add = Room(name=room_name)
        db.session.add(room_to_add)
        db.session.commit()
        return 201

    def get(self, room_name):
        if not room_name_exists(room_name):
            abort(403, message="the room {} you are trying to get does not exists".format(room_name))
        result = db.session.query(Room.name).filter_by(name=room_name).one()
        return room_schema.dump(result)

    def put(self, room_name):
        if not room_name_exists(room_name):
            abort(403, message="the room {} you are trying to update does not exists".format(room_name))
        args = room_post_parser.parse_args()
        if room_name_exists(args['name']):
            abort(403, message="the name {} already exists".format(args['name']))
        room_to_update = db.session.query(Room).get(room_name)
        room_to_update.name = args['name']
        db.session.add(room_to_update)
        db.session.commit()

    def delete(self, room_name):
        if not room_name_exists(room_name):
            abort(403, message="the room {} you are trying to delete does not exists".format(room_name))
        room_to_delete = db.session.query(Room).get(room_name)
        db.session.delete(room_to_delete)
        db.session.commit()
        return 200