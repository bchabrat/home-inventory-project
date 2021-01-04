from flask_httpauth import HTTPTokenAuth
from model.models import *
from flask import request

auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(Authorization):
    token = request.headers['Authorization']
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True

