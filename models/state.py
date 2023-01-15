#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    class State(BaseModel, Base):
        """ State class """

        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', cascade="all, delete", backref='state')
else:
    class State(BaseModel):
        # def __init__(self, *args, **kwargs):
        # """initializes state"""
        # super().__init__(*args, **kwargs)
        @property
        def cities(self):
            """City objects getter"""

            from models import storage
            from models.city import City
            related_cities = []
            objects = storage.all(City)
            for key, value in objects.items():
                if value.state_id == self.id:
                    related_cities.append(value)
            return related_cities
