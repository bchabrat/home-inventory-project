from flask import Flask  # import flask
from flask_restful import Api, reqparse, Resource, abort
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.exc import IntegrityError

from flask_cors import CORS

app = Flask(__name__)  # create an app instance
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:new_password@localhost/house_inventory'
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app, resources={r"/*": {"origins": "*"}})