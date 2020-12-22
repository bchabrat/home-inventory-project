import unittest
from Resources.room import *
from Resources.container import *
from Resources.item import *


class TestMain(unittest.TestCase):

    def setUp(self):
        self.room1 = room.Room("living room", 1)
        self.room2 = room.Room("kitchen", 2)
        self.container1 = container.Container("boite plastique", "C1")
        self.container2 = container.Container("folder", "C2")
        self.item1 = item.Item("pen","I1","stationary")
        self.item2 = item.Item("cables", "I2", "connectique")

    def test_room(self):
        # test add_container
        self.room1.add_container(self.container1)
        self.assertEqual(1,len(self.room1.container_list))
        self.room1.add_container(self.container2)
        self.assertEqual(2,len(self.room1.container_list))
        # test remove_container
        self.room1.remove_container(self.container2)
        self.assertEqual(1, len(self.room1.container_list))
        self.assertEqual(self.room1.container_list[0].name,"boite plastique")
        # test add_item
        self.room1.add_item(self.item2)
        self.assertEqual(1, len(self.room1.item_list))
        # test remove_item
        self.assertEqual(self.room1.item_list[0].name, "cables")
        self.room1.remove_item(self.item2)
        self.assertEqual(0, len(self.room1.item_list))
        # captured_output = io.StringIO()  # Create StringIO object
        # sys.stdout = captured_output  # and redirect stdout.
        # self.room1.remove_container(self.container2)  # Call function.
        # sys.stdout = sys.__stdout__ #reset stdout
        # self.assertEqual(captured_output.getvalue(),"folder not in list")

    def test_container(self):
        self.container3 = container.Container("cardboard box", "C3")
        #test add_container
        self.container1.add_container(self.container2)
        self.assertEqual(1, len(self.container1.container_list))
        # test add_item
        self.container1.add_item(self.item1)
        self.assertEqual(1, len(self.container1.item_list))
        # test remove_item
        self.container1.remove_item(self.item1)
        self.assertEqual(0, len(self.container1.item_list))
        # test remove_container
        self.container1.remove_container(self.container2)
        self.assertEqual(0, len(self.container1.container_list))
        # test move_container_from_container
        self.container1.add_container(self.container2)
        self.container2.move_container_from_container(self.container1, self.container3)
        self.assertEqual(self.container3.container_list[0].name, "folder")
        # test move_container_from_room
        self.room1.add_container(self.container1)
        self.container1.move_container_from_room(self.room1, self.room2)
        self.assertEqual(self.room2.container_list[0].name, "boite plastique")

    def test_item(self):
        self.container3 = container.Container("cardboard box", "C3")
        # test move_container_from_container
        self.container1.add_item(self.item1)
        self.item1.move_item_from_container(self.container1, self.container3)
        self.assertEqual(self.container3.item_list[0].name, "pen")
        # test move_container_from_room
        self.room1.add_item(self.item1)
        self.item1.move_item_from_room(self.room1, self.room2)
        self.assertEqual(self.room2.item_list[0].name, "pen")