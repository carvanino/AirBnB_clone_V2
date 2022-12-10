#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.review import Review
# from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

metadata = Base.metadata

"""
place_amenity = Table('place_amenity', metadata,
        Column('place_id', String(60), ForeignKey('places.id'),
            primary_key=True, nullable=False),
        Column('amenity_id', String(60), ForeignKey('amenities.id'),
            primary_key=True, nullable=False))
"""


if getenv('HBNB_TYPE_STORAGE') == 'db':
    class Place(BaseModel, Base):
        """ A place to stay """

        __tablename__ = 'places'

        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        reviews = relationship('Review', cascade='delete', backref='place')

        place_amenity = Table(
                'place_amenity', metadata,
                Column(
                    'place_id', String(60), ForeignKey('places.id'),
                    primary_key=True, nullable=False),
                Column(
                    'amenity_id',
                    String(60), ForeignKey('amenities.id'),
                    primary_key=True, nullable=False))

        amenities = relationship(
                'Amenity', secondary=place_amenity,
                viewonly=False)
else:
    class Place(BaseModel):
        """ A place to stay """
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
            reviewList = []
            reviews = storage.all('Review')
            for key, value in reviews.items():
                if self.id == value.place_id:
                    reviewList.append(value)
            return reviewList

        @property
        def amenities(self):
            amenity_list = []
            amenities = storage.all('Amenity')
            for key, value in amenities.items():
                if value.id == self.amenity_ids:
                    amenity_list.append(value)
            return amenity_list

        @amenities.setter
        def amenities(self, obj):
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
