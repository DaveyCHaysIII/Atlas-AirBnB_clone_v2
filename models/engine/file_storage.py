#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """Returns a dictionary of models currently in storage"""
        return self.__objects

    def new(self, obj):
        """Stores an object in objects"""
        # format the key for instance storage
        key = f"{obj.__class__.__name__}.{obj.id}"
        # add the instance strings to the objects dictionary
        self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file specified in __file_path"""
        # initialize an empty dictionar
        obj_dict = {}
        for k, v in self.__objects.items():
            # convert and store instance strings as attribute dictionaries
            obj_dict[k] = v.to_dict()
            # open or create json file to store new dictionary
        with open(self.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Loads storage dictionary from file"""
        # check the json file exists
        if os.path.exists(self.__file_path):
            with open(self.__file_path, "r", encoding="utf-8") as f:
                for k, v in json.load(f).items():
                    self.new(classes[v.get('__class__')](**v))
