from flask import g,jsonify,abort
from flask_restful import Api, reqparse, Resource, abort
from model.models import *
from . import auth

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str)
login_parser.add_argument('password', type=str)

def verify_password(username,password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True



user_schema = UserSchema()


class NewUserResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        username = args['username']
        password = args['password']
        if username is None or password is None:
            abort(400,message="missing arguments")
        if User.query.filter_by(username=username).first() is not None:
            abort(400, message="existing user")
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return 201


class TokenResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        verified = verify_password(args['username'],args['password'])
        if verified == True:
            token = g.user.generate_auth_token()
            return {'token': token.decode('ascii')}
        abort(401)







