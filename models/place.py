#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base
from models.review import Review


class Place(BaseModel, Base):
    """ A place to stay """
    if models.storage_t == 'db':
        __tablename__ = 'places'

        place_amenity = Table(
            'place_amenity',
            Base.metadata,
            Column(
                'place_id',
                String(60),
                ForeignKey('places.id', ondelete='CASCADE'),
                primary_key=True,
                nullable=False),
            Column(
                'amenity_id',
                String(60),
                ForeignKey('amenities.id', ondelete='CASCADE'),
                primary_key=True,
                nullable=False))

        city_id = Column(
            String(60),
            ForeignKey('cities.id'),
            nullable=False)
        user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False)
        name = Column(
            String(128),
            nullable=False)
        description = Column(
            String(1024),
            nullable=True)
        number_rooms = Column(
            Integer,
            default=0,
            nullable=False)
        number_bathrooms = Column(
            Integer,
            default=0,
            nullable=False)
        max_guest = Column(
            Integer,
            default=0,
            nullable=False)
        price_by_night = Column(
            Integer,
            default=0,
            nullable=False)
        latitude = Column(
            Float,
            nullable=True)
        longitude = Column(
            Float,
            nullable=True)

        amenities = relationship(
            'Amenity',
            secondary='place_amenity',
            back_populates='place_amenities',
            cascade='all, delete-orphan',
            viewonly=False)
        reviews = relationship(
            'Review',
            backref='place',
            cascade='all, delete-orphan')

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

    @property
    def reviews(self):
        """ getter for reviews"""
        from models import storage
        review_list = []
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == self.id:
                review_list.append(review)
        return review_list

    @property
    def amenities(self):
        """ getter for amenities"""
        from models import storage
        from models.amenity import Amenity  # Delayed import
        amenity_list = []
        all_amenities = storage.all(Amenity)
        for amenity in all_amenities.values():
            if amenity.place_id == self.id:
                amenity_list.append(amenity)
        return amenity_list

    @amenities.setter
    def amenities(self, value):
        """Setter for amenities in FileStorage"""
        from models.amenity import Amenity  # Delayed import
        if isinstance(value, Amenity):
            if value.id not in self.amenity_ids:
                self.amenity_ids.append(value.id)
        else:
            return
