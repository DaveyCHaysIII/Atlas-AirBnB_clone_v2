#!/usr/bin/python3
import unittest
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel, Base
from models.user import User
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the tests"""
        # Set environment variables for the test database
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
        os.environ['HBNB_ENV'] = 'test'

        # Initialize the storage
        cls.storage = DBStorage()
        cls.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Tear down after the tests"""
        cls.storage._DBStorage__session.close()

    def setUp(self):
        """Set up for individual tests"""
        self.session = self.storage._DBStorage__session

    def tearDown(self):
        """Clean up after individual tests"""
        self.session.rollback()
        for table in reversed(Base.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_adds_obj(self):
        """Test that new adds an object to the session"""
        user = User(email="test@test.com", password="test_pwd")
        self.storage.new(user)
        self.assertIn(user, self.session.new)

    def test_save_commits_session(self):
        """Test that save commits the session"""
        user = User(email="test@test.com", password="test_pwd")
        self.storage.new(user)
        self.storage.save()
        self.assertNotIn(user, self.session.new)

    def test_delete_removes_obj(self):
        """Test that delete removes an object from the session"""
        user = User(email="test@test.com", password="test_pwd")
        self.storage.new(user)
        self.storage.save()
        self.storage.delete(user)
        self.assertIn(user, self.session.deleted)

    def test_reload(self):
        """Test that reload recreates the session"""
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)

    def test_all_with_class(self):
        """Test that all returns objects of a given class"""
        user1 = User(email="test1@test.com", password="test_pwd")
        user2 = User(email="test2@test.com", password="test_pwd")
        self.storage.new(user1)
        self.storage.new(user2)
        self.storage.save()
        users = self.storage.all(User)
        self.assertEqual(len(users), 2)
        self.assertIn(f"User.{user1.id}", users)
        self.assertIn(f"User.{user2.id}", users)

if __name__ == '__main__':
    unittest.main()