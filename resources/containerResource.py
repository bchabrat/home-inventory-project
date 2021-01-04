from flask_restful import Api, reqparse, Resource, abort
from model.models import *
from . import auth

container_parser = reqparse.RequestParser()
container_parser.add_argument('id', type=int)
container_parser.add_argument('name', type=str, help=' name of the container')
container_parser.add_argument('new_name', type=str, help='new name of the container')
container_parser.add_argument('room_id', type=int, help='id of the room where the container is located')
container_parser.add_argument('container_id', type=int, help='id of the container where the container is located')

container_schema = ContainerSchema()
containers_schema = ContainerSchema(many=True)


def container_name_exists(container_name):
    names = [item.name for item in db.session.query(Container).filter_by(user_id=g.user.id).all()]
    if container_name in names:
        return True
    return False

def container_id_exists(container_id):
    ids = [item.id for item in db.session.query(Container).filter_by(user_id=g.user.id).all()]
    if container_id in ids:
        return True
    return False


# get a list of all the containers
class AllContainerResource(Resource):
    @auth.login_required
    def get(self):
        result = db.session.query(Container).filter_by(user_id=g.user.id).join(Containers.room).all()
        return containers_schema.dump(result)


# create, read, update and delete a container
class ContainerResource(Resource):
    @auth.login_required
    def post(self):
        args = container_parser.parse_args()
        if container_name_exists(args['name']):
            abort(403, message="the name {} already exists".format(args['name']))

        item_to_add = Container(name=args['name'], room_id=args['room_id'], container_id=args['container_id'],user_id=g.user.id)
        db.session.add(item_to_add)
        db.session.commit()
        return 201

    @auth.login_required
    def get(self):
        args = container_parser.parse_args()
        if not container_id_exists(args['id']):
            abort(403, message="the container {} you are trying to get does not exists".format(args['name']))
        result = db.session.query(Container).filter_by(name=args['name']).one()
        return container_schema.dump(result)

    @auth.login_required
    def put(self):
        args = container_parser.parse_args()
        if not container_id_exists(args['id']):
            abort(403, message="the container {} you are trying to update does not exists".format(args['name']))
        if container_name_exists(args['new_name']):
            abort(403, message="the name {} already exists".format(args['new_name']))
        container_to_update = db.session.query(Container).get(args['id'])
        if args['new_name'] is not None:
            container_to_update.name = args['new_name']
        if args['container_id'] is not None:
            container_to_update.container_id = args['container_id']
        if args['room_id'] is not None:
            container_to_update.room_id = args['room_id']
        db.session.add(container_to_update)
        db.session.commit()

    @auth.login_required
    def delete(self):
        args = container_parser.parse_args()
        if not container_id_exists(args['id']):
            abort(403, message="the container {} you are trying to delete does not exists".format(args['name']))
        container_to_delete = db.session.query(Container).get(args['id'])
        try:
            db.session.delete(container_to_delete)
            db.session.commit()
            return 200
        except IntegrityError:
            abort(403, message="please delete amy child item first")
