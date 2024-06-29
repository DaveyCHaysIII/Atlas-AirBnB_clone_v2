#!/usr/bin/python3
"""
    This module defines a class to manage database storage for hbnb clone
"""
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel


class DBStorage:
    """Manages storage of HBNB models in a MySQL database"""
    __engine = None
    __session = None


    def __init__(self):
        """Initialize the database engine and session"""
        user = os.getenv('HBNB_MYSQL_USER')
        password = os.getenv('HBNB_MYSQL_PWD')
        host = os.getenv('HBNB_MYSQL_HOST', 'localhost')
        database = os.getenv('HBNB_MYSQL_DB')
        env = os.getenv('HBNB_ENV')

        self.__engine = create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{database}',
                                      pool_pre_ping=True)

        if env == 'test':
            BaseModel.metadata.drop_all(self.__engine)

        self.reload()

    def all(self, cls=None):
        """Query all objects in the current database session"""
        if cls:
            objs = self.__session.query(cls).all()
        else:
            objs = []
            for class_ in [User, State, City, Amenity, Place, Review]:  # Import these models
                objs.extend(self.__session.query(class_).all())
        return {f'{type(obj).__name__}.{obj.id}': obj for obj in objs}

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload all tables and create the current database session"""

        BaseModel.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

# Example models/base_model.py

from sqlalchemy.ext.declarative import declarative_base
