#!/usr/bin/python3
"""This module defines a class User"""
from sqlalchemy import Column, String
from models import storage_t
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if storage_t == 'db':
        __tablename__ = 'users'
        places = relationship(
            "Place", 
            backref='user', 
            cascade="all, delete-orphan"
            )
        email = Column(
            String(128),
            nullable=False
        )
        password = Column(
            String(128),
            nullable=False
        )
        first_name = Column(
            String(128),
            nullable=False
        )
        last_name = Column(
            String(128),
            nullable=False
        )
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
