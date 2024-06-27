#!/usr/bin/python3
"""
    This module defines tests for the HBNBConsole
"""

import unittest
from unittest.mock import patch, MagicMock
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from console import HBNBCommand


class TestHBNBConsole(unittest.TestCase):

    """
        Set up base model with MagicMock to demonstrate
        object initialization, persistence, and deletion.
    """
    @classmethod
    def setUpClass(cls):
        cls.cmd = HBNBCommand()
        cls.storage_mock = MagicMock(spec=BaseModel)
        cls.storage_mock.save.return_value = None

    """
        Test creation of a new object.
    """
    @patch('models.storage')
    def test_do_create(self, mock_storage):
        mock_storage._FileStorage__objects.clear()
        self.cmd.do_create('User')
        self.assertIn('User', mock_storage._FileStorage__objects.keys())
        self.assertIsInstance(mock_storage._FileStorage__objects['User'], User)

    """
        Test object retrieval after creation.
    """
    @patch('models.storage')
    def test_do_show(self, mock_storage):
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(id='1')
        result = self.cmd.do_show('User 1')
        expected_output = "<User; id=1>"
        self.assertEqual(result, expected_output)

    """
        Test destruction of objects.
    """
    @patch('models.storage')
    def test_do_destroy(self, mock_storage):
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(id='1')
        self.cmd.do_destroy('User 1')
        self.assertNotIn('User.1', mock_storage._FileStorage__objects.keys())

    """
        Test update of object attributes.
    """
    @patch('models.storage')
    def test_do_update(self, mock_storage):
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(id='1')
        self.cmd.do_update('User 1', 'name', 'New Name')
        updated_user = mock_storage._FileStorage__objects['User.1']
        self.assertEqual(updated_user.name, 'New Name')

    """
        Test accurate object count.
    """
    @patch('models.storage')
    def test_do_count(self, mock_storage):
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(id='1')
        mock_storage._FileStorage__objects['Place.2'] = Place(id='2')
        self.assertEqual(self.cmd.do_count(), 2)


if __name__ == '__main__':
    unittest.main()
