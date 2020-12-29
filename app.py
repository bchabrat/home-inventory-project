import Main
from flask import Flask  # import flask
from flask_restful import Api, reqparse, Resource, abort
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from Main.Service.roomResource import *
from Main.Service.containerResource import *
from Main.Service.itemResource import *
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from Main import api

api.add_resource(AllRoomResource, '/list_rooms')
api.add_resource(RoomResource, '/room/<string:room_name>')
api.add_resource(AllContainerResource, '/list_containers')
api.add_resource(ContainerResource, '/container/<string:container_name>')
api.add_resource(AllItemResource, '/list_items')
api.add_resource(ItemResource, '/item/<string:item_name>')


