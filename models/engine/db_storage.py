#!/usr/bin/python3
"""
    This module defines a class to manage database storage for hbnb clone
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


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
        from models.base_model import BaseModel

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        self.reload()

    def all(self, cls=None):
        """Query all objects in the current database session"""
        objs = {}
        if cls:
            # If class specified, query all objects of that class
            results = self.__session.query(cls).all()
            for obj in results:
                key = f"{cls.__name__}.{obj.id}"
                objs[key] = obj
        else:
            # If no class specified, query objects of all classes
            classes = [User, State, City, Amenity, Place, Review]
            for class_ in classes:
                results = self.__session.query(class_).all()
                for obj in results:
                    key = f"{class_.__name__}.{obj.id}"
                    objs[key] = obj
        return objs

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

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """adds close method to close out session"""
        self.__session.close()
