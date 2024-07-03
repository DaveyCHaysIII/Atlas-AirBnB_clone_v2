#!/usr/bin/python3
""" Review module for the HBNB project """
from sqlalchemy import Column, String, ForeignKey
from models import storage_t
from models.base_model import BaseModel, Base


class Review(BaseModel, Base):
    """ Review classto store review information """
    if storage_t == 'db':
        __tablename__ = 'reviews'

        place_id = Column(
            String(60),
            ForeignKey('places.id', ondelete='CASCADE'),
            nullable=False)
        user_id = Column(
            String(60),
            ForeignKey('users.id', ondelete='CASCADE'),
            nullable=False)
        text = Column(
            String(1024),
            nullable=False)

    else:
        place_id = ""
        user_id = ""
        text = ""
