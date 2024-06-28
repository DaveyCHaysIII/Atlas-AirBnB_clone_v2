#!/usr/bin/python3

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


class TestHBNBCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize the console command
        cls.cmd = HBNBCommand()
        # Mock the storage module to avoid persisting changes to disk
        cls.storage_mock = MagicMock(spec=FileStorage)
        cls.storage_mock.save.return_value = None

    @patch('console.HBNBCommand.storage', new_callable=MagicMock)
    def test_do_create(self, mock_storage):
        """
        Test the do_create command to ensure it creates a new instance.
        """
        # Setup: Mock the storage to simulate creating a new instance
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(id='1')
        # Action: Call the do_create command
        self.cmd.onecmd("create User name=test_user")
        # Assert: Verify that the new instance was added to storage
        self.assertIn('User.1', mock_storage._FileStorage__objects.keys())
        # Assert: Verify that the instance has the correct attributes
        user_instance = mock_storage._FileStorage__objects['User.1']
        self.assertEqual(user_instance.name, 'test_user')

    @patch('console.HBNBCommand.storage', new_callable=MagicMock)
    def test_do_show(self, mock_storage):
        """
        Test the do_show command to ensure it displays the correct instance.
        """
        # Setup: Mock the storage to simulate existing instances
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(
            id='1', name='test_user')
        # Action: Call the do_show command
        result = self.cmd.onecmd("show User 1")
        # Assert: Verify that the output matches the expected instance details
        expected_output = "<User; id=1; name=\"test_user\">"
        self.assertEqual(result, expected_output)

    @patch('console.HBNBCommand.storage', new_callable=MagicMock)
    def test_do_destroy(self, mock_storage):
        """
        Test the do_destroy command to ensure it removes an instance.
        """
        # Setup: Mock the storage to simulate existing instances
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(
            id='1', name='test_user')
        # Action: Call the do_destroy command
        self.cmd.onecmd("destroy User 1")
        # Assert: Verify that the instance was removed from storage
        self.assertNotIn('User.1', mock_storage._FileStorage__objects.keys())

    @patch('console.HBNBCommand.storage', new_callable=MagicMock)
    def test_do_all(self, mock_storage):
        """
        Test the do_all command to ensure it lists all instances.
        """
        # Setup: Mock the storage to simulate multiple instances
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(
            id='1', name='test_user')
        mock_storage._FileStorage__objects['User.2'] = User(
            id='2', name='another_test_user')
        # Action: Call the do_all command
        result = self.cmd.onecmd("all")
        # Assert: Verify that the output includes details for both instances
        expected_output = """<User; id=1; name=\"test_user\">
        <User; id=2; name=\"another_test_user\">"""
        self.assertEqual(result, expected_output)

    @patch('console.HBNBCommand.storage', new_callable=MagicMock)
    def test_do_count(self, mock_storage):
        """
        Test the do_count command to ensure it counts instances correctly.
        """
        # Setup: Mock the storage to simulate multiple instances
        mock_storage._FileStorage__objects.clear()
        mock_storage._FileStorage__objects['User.1'] = User(
            id='1', name='test_user')
        mock_storage._FileStorage__objects['User.2'] = User(
            id='2', name='another_test_user')
        # Action: Call the do_count command
        result = self.cmd.onecmd("count User")
        # Assert: Verify that the output matches the number of instances
        self.assertEqual(result, "2")


if __name__ == '__main__':
    unittest.main()
