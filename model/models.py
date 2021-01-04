from flask import g,current_app
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


db = SQLAlchemy()
ma = Marshmallow()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')
    username = db.Column(db.String(100), index=True)
    password_hash = db.Column(db.String(255))

    rooms = relationship("Room", back_populates="user")
    containers = relationship("Container", back_populates="user")
    items = relationship("Item", back_populates="user")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class Room(db.Model):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)

    user = relationship("User", back_populates="rooms")
    containers = relationship("Container", back_populates='room')
    items = relationship("Item", back_populates='room')

    def __repr__(self):
        return f'<Room> name = {self.name}'


class Container(db.Model):
    __tablename__ = 'containers'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    container_id = Column(Integer, ForeignKey('containers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    room = relationship("Room", back_populates="containers")
    items = relationship("Item", back_populates='container')
    user = relationship("User", back_populates="containers")

    # container = relationship("Container", back_populates='containers')


class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    room_id = Column(Integer, ForeignKey('rooms.id'))
    container_id = Column(Integer, ForeignKey('containers.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    room = relationship("Room", back_populates="items")
    container = relationship("Container", back_populates='items')
    user = relationship("User", back_populates="items")


class RoomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Room
        include_fk = True


class ContainerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Container
        include_fk = True


class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

