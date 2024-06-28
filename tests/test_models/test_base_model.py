#!/usr/bin/python3
"""
    This module defines tests for BaseModel
"""
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """
        Class holding unit tests for the BaseModel class.
    """

    def __init__(self, *args, **kwargs):
        """
            Initialize the test class.
        """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        pass

    def tearDown(self):
        """
            Clean up the working environment after each test.
        """
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """
            Tests instance type is BaseModel
        """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """
            Test copying an instance using kwargs
            creates a new instance.
        """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """
            Tests passing an integer key in kwargs
            raises a TypeError.
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """
            Tests saving an instance accurately
            serializes attributes to json file
        """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """
            Tests string representation is formatted correctly
        """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_to_dict(self):
        """
            Verifies to_dict accurately stores attributes
            as expected in dictionary format
        """
        i = self.value()
        dictionary = i.to_dict()
        self.assertEqual(dictionary["__class__"], i.__class__.__name__)
        self.assertEqual(dictionary["id"], i.id)
        self.assertEqual(dictionary["created_at"], i.created_at.isoformat())
        self.assertEqual(dictionary["updated_at"], i.updated_at.isoformat())

    def test_kwargs_none(self):
        """
            Test that passing None as a key in kwargs
            raises a TypeError.
        """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """
        Test that BaseModel accepts and stores arbitrary attributes.
        """
        n = {'Name': 'test'}
        instance = BaseModel(**n)
        self.assertEqual(instance.Name, 'test')

    def test_id(self):
        """
            Tests that id attribute is a string.
        """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """
            Tests that created_at attribute is a datetime object
        """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """
            Tests that updated_at attribute is a datetime object
            that updates when changes are made.
        """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_init_from_dict(self):
        """
            Test initializing an instance from a dictionary
            preserves its attributes.
        """
        obj = self.value()
        obj_2 = self.value()
        self.assertNotEqual(obj.id, obj_2.id)
        json_obj = self.value(**obj.to_dict())
        self.assertEqual(obj.id, json_obj.id)
        self.assertEqual(obj.created_at, json_obj.created_at)
        self.assertEqual(obj.updated_at, json_obj.updated_at)

if __name__ == '__main__':
    unittest.main()