#!/usr/bin/python3

import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):

    @classmethod
    def setUp(self):
        # Initialize the console command
        self.cmd = HBNBCommand()
        # Capture sys.stdout for verifying test output
        self.mock_stdout = StringIO()
        self.patch_stdout = patch("sys.stdout", self.mock_stdout)

    def tearDown(self):
        # Close StringIO and stop output capture
        self.patch_stdout.stop()
        self.mock_stdout.close()
        #  Clear FileStorage
        storage._FileStorage__objects.clear()

    def test_do_create(self):
        """
            Test the do_create command to ensure it creates a new instance.
        """

        with self.patch_stdout:
            # Run create User
            self.cmd.onecmd("create User")
            output = self.mock_stdout.getvalue().strip()
            # Check that captured output is not 0
            self.assertTrue(len(output) > 0)

            # Check storage for created User obj
            stored = storage.all()
            expected_key = f"User.{output}"
            self.assertIn(expected_key, stored)
       

    def test_do_show(self):
        """
            Test the do_show command to ensure it displays the correct instance.
        """
        with self.patch_stdout:
            # Run create User
            self.cmd.onecmd("create User")
            # Capture id from output
            cr_output = self.mock_stdout.getvalue().strip()
            # Clear mock output buffer
            self.mock_stdout.truncate(0)
            self.mock_stdout.seek(0)
            # Run show User and capture output
            self.cmd.onecmd("show User " + cr_output)
            sh_output = self.mock_stdout.getvalue().strip()
            # Check that instance was found
            self.assertFalse(sh_output == "** no instance found **")

    def test_do_destroy(self):
        """
            Test the do_destroy command to ensure it removes an instance.
        """
        with self.patch_stdout:
            # Run create User and capture id
            self.cmd.onecmd("create User")
            cr_output = self.mock_stdout.getvalue().strip()
            # Run destroy User and clear mock output buffer
            self.cmd.onecmd("destroy User " + cr_output)
            self.mock_stdout.truncate(0)
            self.mock_stdout.seek(0)
            # Run show User with captured id
            self.cmd.onecmd("show User " + cr_output)
            # Capture output and check that no instance found
            sh_output = self.mock_stdout.getvalue().strip()
            self.assertTrue(sh_output == "** no instance found **")

    def test_do_all(self):
        """
            Test the do_all command to ensure it lists all instances.
        """
        with self.patch_stdout:
            # Run create User and capture id
            self.cmd.onecmd("create User")
            cr_output1 = self.mock_stdout.getvalue().strip()
            # Clear mock output buffer
            self.mock_stdout.truncate(0)
            self.mock_stdout.seek(0)

            # Run creat user anc capture second id
            self.cmd.onecmd("create User")
            cr_output2 = self.mock_stdout.getvalue().strip()
            # Clear mock output buffer
            self.mock_stdout.truncate(0)
            self.mock_stdout.seek(0)

            # Run all User and capture output
            self.cmd.onecmd("all User")
            all_output = self.mock_stdout.getvalue().strip()

            # Ensure captured ids are present in output
            self.assertIn(f"[User] ({cr_output1})", all_output)
            self.assertIn(f"[User] ({cr_output2})", all_output)

    def test_do_count(self):
        """
            Test the do_count command to ensure it counts instances correctly.
        """
        with self.patch_stdout:
            # Run create User twice
            self.cmd.onecmd("create User")
            self.cmd.onecmd("create User")
            # Clear mock output buffer
            self.mock_stdout.truncate(0)
            self.mock_stdout.seek(0)

            # Run count User
            self.cmd.onecmd("count User")
            # Ensure captured output is '2'
            self. assertEqual(self.mock_stdout.getvalue().strip(), '2')


if __name__ == '__main__':
    unittest.main()
