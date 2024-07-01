#!/usr/bin/python3
""" State Module for HBNB project """
from sqlalchemy import Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models import storage_t
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    if storage_t == 'db':
        from models.place import place_amenity
        __tablename__ = 'amenities'
        name = Column(
            String(128),
            nullable=False
        )
        place_amenities = relationship(
            "Place",
            secondary=place_amenity,
            back_populates="amenities")
    else:
        name = ""
