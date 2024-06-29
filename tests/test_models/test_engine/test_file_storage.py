#!/usr/bin/python3
""" Module for testing file storage"""
import unittest
import os
from models.base_model import BaseModel
from models.user import User
from models import storage
from models.engine.file_storage import FileStorage


class test_fileStorage(unittest.TestCase):
    """ Class to test the file storage method """

    def setUp(self):
        """set up for testing"""
        self.file_path = 'file_test.json'
        self.storage = storage
        self.storage.set_file_path(self.file_path)
        self.obj = BaseModel()
        self.obj2 = User()

    def tearDown(self):
        """file cleanup after testing"""
        self.storage.objects.clear()
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_storage_var_created(self):
        """ FileStorage object storage created """
        self.assertEqual(type(self.storage), FileStorage)

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(self.storage.file_path), str)

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(self.storage.all()), dict)

    def test_new(self):
        """Tests to make sure objects are stored as dictionary objects"""
        k = f"{self.obj.__class__.__name__}.{self.obj.id}"
        self.storage.new(self.obj)
        self.assertIn(k, self.storage.all())

    def test_all_no_cls(self):
        """tests the all method with no cls specified"""
        k1 = f"{self.obj.__class__.__name__}.{self.obj.id}"
        k2 = f"{self.obj2.__class__.__name__}.{self.obj2.id}"
        self.storage.new(self.obj)
        self.storage.new(self.obj2)
        objs = self.storage.all()
        self.assertEqual(objs[k1], self.obj)
        self.assertEqual(objs[k2], self.obj2)

    def test_all_cls(self):
        """tests the all method with cls specified"""
        k1 = f"{self.obj.__class__.__name__}.{self.obj.id}"
        k2 = f"{self.obj2.__class__.__name__}.{self.obj2.id}"
        self.storage.new(self.obj)
        self.storage.new(self.obj2)
        BMs = self.storage.all(BaseModel)
        Us = self.storage.all(User)
        self.assertIn(k1, BMs)
        self.assertNotIn(k1, Us)
        self.assertIn(k2, Us)
        self.assertNotIn(k2, BMs)

    def test_base_model_instantiation(self):
        """ File is not created on BaseModel save """
        new = BaseModel()
        self.assertFalse(os.path.exists('file_test.json'))

    def test_save(self):
        """Tests that save serializes object to json file"""
        k = f"{self.obj.__class__.__name__}.{self.obj.id}"
        self.storage.new(self.obj)
        self.storage.save()
        self.assertTrue(os.path.exists('file_test.json'))
        self.assertEqual(self.storage.all()[k].id, self.obj.id)

    def test_reload(self):
        """Tests that save serializes object to json file
            and reload correctly deserializes object data"""
        k = f"{self.obj.__class__.__name__}.{self.obj.id}"
        self.storage.new(self.obj)
        self.storage.save()
        storage_2 = FileStorage()
        storage_2.reload()
        reloaded_obj = storage_2.all()[k]
        self.assertEqual(reloaded_obj.id, self.obj.id)
        self.assertEqual(reloaded_obj.to_dict(), self.obj.to_dict())

    def test_reload_empty(self):
        """ Load from an empty file """
        self.storage.new(self.obj)
        self.storage.save()
        with open('file_test.json', 'w') as f:
            pass
        with self.assertRaises(ValueError):
            self.storage.reload()

    def test_reload_from_nonexistent(self):
        """ Nothing happens if file does not exist """
        self.assertEqual(self.storage.reload(), None)

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        self.obj.save()
        self.assertTrue(os.path.exists('file_test.json'))

    def test_file_path(self):
        """Tests file creation on save using file_path"""
        self.assertFalse(os.path.exists(self.file_path))
        self.storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_key_format(self):
        """ Key is properly formatted """
        _id = self.obj2.to_dict()['id']
        for key in self.storage.all().keys():
            temp = key
        self.assertEqual(temp, 'User' + '.' + _id)
