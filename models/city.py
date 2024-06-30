#!/usr/bin/python3
""" City Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models import storage_t
from models.base_model import BaseModel, Base


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    if storage_t == 'db':
        __tablename__ = 'cities'
        places = relationship(
            "Place", 
            backref='cities', 
            cascade="all, delete-orphan")
        name = Column(
            String(128),
            nullable=False)
        state_id = Column(
            String(60),
            ForeignKey('states.id'),
            nullable=False)
    else:
        state_id = ''
        name = ''
