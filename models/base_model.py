#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import models
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, String

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

        else:
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    # convert string values to formatted datetime objects
                    v = datetime.strptime(v, time_format)
                if k != '__class__':
                    # set all attributes except for class
                    setattr(self, k, v)
                if "id" not in kwargs:
                    # supply id and timestamps for new instances from kwargs
                    self.id = str(uuid.uuid4())
                    self.created_at = datetime.now()
                    self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary["__class__"] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        from models import storage
        storage.delete(self)
