from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


class Room(db.Model):
    __tablename__ = 'rooms'
    name = Column(String, primary_key=True)
    containers = relationship("Container", back_populates='room')
    items = relationship("Item", back_populates='room')

    def __repr__(self):
        return f'<Room> name = {self.name}'


class Container(db.Model):
    __tablename__ = 'containers'
    name = Column(String, primary_key=True)
    room_name = Column(String, ForeignKey('rooms.name'))
    container_name = Column(String, ForeignKey('containers.name'))
    room = relationship("Room", back_populates="containers")
    items = relationship("Item", back_populates='container')
    # container = relationship("Container", back_populates='containers')


class Item(db.Model):
    __tablename__ = 'items'
    name = Column(String, primary_key=True)
    room_name = Column(String, ForeignKey('rooms.name'))
    container_name = Column(String, ForeignKey('containers.name'))
    room = relationship("Room", back_populates="items")
    container = relationship("Container", back_populates='items')


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

