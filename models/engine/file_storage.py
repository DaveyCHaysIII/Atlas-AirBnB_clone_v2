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

    @property
    def file_path(self):
        """Getter for the file path."""
        return self.__file_path

    @property
    def objects(cls):
        """Getter for the objects dictionary."""
        return cls.__objects

    def set_file_path(self, path):
        """setter for the file_path"""
        if isinstance(path, str):
            self.__file_path = path
        else:
            raise ValueError("file_path must be a string.")

    def all(self, cls=None):
        """
            Returns a dictionary of models currently in storage.
            if the cls optional arg is supplied, returns a dictionary
            of objects of that class currently stored.
        """
        if cls:
            obj_dict = {}
            for k, v in self.__objects.items():
                if v.__class__.__name__ == cls.__name__:
                    obj_dict[k] = v
            return obj_dict
        else:
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
            try:
                with open(self.__file_path, "r", encoding="utf-8") as f:
                    for k, v in json.load(f).items():
                        self.new(classes[v.get('__class__')](**v))
            except json.JSONDecodeError:
                raise ValueError

    def delete(self, obj=None):
        """
            Deletes a specified object from __objects if it exists.
            If obj is unspecified, does nothing.
        """
        if obj:
            k = f"{obj.__class__.__name__}.{obj.id}"
            if k in self.__objects:
                del self.__objects[k]

    def close(self):
        """calls reload for reasons that escape me"""
        self.reload()
