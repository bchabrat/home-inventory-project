from .. import api

api.add_resource(AllRoomResource, '/list_rooms')
api.add_resource(RoomResource, '/room/<string:room_name>')
api.add_resource(AllContainerResource, '/list_containers')
api.add_resource(ContainerResource, '/container/<string:container_name>')
api.add_resource(AllItemResource, '/list_items')
api.add_resource(ItemResource, '/item/<string:item_name>')
