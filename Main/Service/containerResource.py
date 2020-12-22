from flask_restful import Api, reqparse, Resource, abort
from Main import db
from Main.model.models import *


container_parser = reqparse.RequestParser()
container_parser.add_argument('name', type=str, help='name of the container')
container_parser.add_argument('room_name', type=str, help='name of the room where the container is located')
container_parser.add_argument('container_name', type=str, help='name of the container where the container is located')
container_schema = ContainerSchema()
containers_schema = ContainerSchema(many=True)


def container_name_exists(container_name):
    names = [item.name for item in db.session.query(Container).all()]
    if container_name in names:
        result = True
    else:
        result = False
    return result


# get a list of all the containers
class AllContainerResource(Resource):
    def get(self):
        result = db.session.query(Container).all()
        return containers_schema.dump(result)


# create, read, update and delete a container
class ContainerResource(Resource):
    def post(self, container_name):
        if container_name_exists(container_name):
            abort(403, message="the name {} already exists".format(container_name))
        args = container_parser.parse_args()
        item_to_add = Container(name=container_name, room_name=args['room_name'], container_name=args['container_name'])
        db.session.add(item_to_add)
        db.session.commit()
        return 201

    def get(self, container_name):
        if not container_name_exists(container_name):
            abort(403, message="the room {} you are trying to get does not exists".format(container_name))
        result = db.session.query(Container).filter_by(name=container_name).one()
        return container_schema.dump(result)

    def put(self, container_name):
        if not container_name_exists(container_name):
            abort(403, message="the container {} you are trying to update does not exists".format(container_name))
        args = container_parser.parse_args()
        if container_name_exists(args['name']):
            abort(403, message="the name {} already exists".format(args['name']))
        container_to_update = db.session.query(Container).get(container_name)
        if args['name'] is not None:
            container_to_update.name = args['name']
        if args['container_name'] is not None:
            container_to_update.container_name = args['container_name']
        if args['room_name'] is not None:
            container_to_update.room_name = args['room_name']
        db.session.add(container_to_update)
        db.session.commit()

    def delete(self, container_name):
        if not container_name_exists(container_name):
            abort(403, message="the container {} you are trying to delete does not exists".format(container_name))
        container_to_delete = db.session.query(Container).get(container_name)
        try:
            db.session.delete(container_to_delete)
            db.session.commit()
            return 200
        except IntegrityError:
            abort(403, message="please delete amy child item first")
