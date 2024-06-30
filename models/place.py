#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_t
from models.base_model import BaseModel


class Place(BaseModel, Base):
    """ A place to stay """
    if storage_t == 'db':
        __tablename__ = 'places'
        city_id = Column()
        user_id = Column()
        name = Column()
        description = Column()
        number_rooms = Column()
        number_bathrooms = Column()
        max_guest = Column()
        price_by_night = Column()
        latitude = Column()
        longitude = Column()
        amenity_ids = Column()


    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []
