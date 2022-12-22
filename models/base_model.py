#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            # from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self)
        else:
            if kwargs.get('id', None) is None:
                self.id = str(uuid.uuid4())

            if kwargs.get('updated_at', None) is not None:
                kwargs['updated_at'] = datetime.\
                    strptime(kwargs['updated_at'],
                             '%Y-%m-%dT%H:%M:%S.%f')

            if kwargs.get('created_at', None) is not None:
                kwargs['created_at'] = datetime.\
                    strptime(kwargs['created_at'],
                             '%Y-%m-%dT%H:%M:%S.%f')

            if kwargs.get('__class__', None) is not None:
                del kwargs['__class__']

            self.__dict__.update(kwargs)
            # for key, value in kwargs.items():
            # setattr(self, key, value)
            # kwargs['updated_at'] = datetime.strptime(kwargs['updated_at']
            # '%Y-%m-%dT%H:%M:%S.%f')
            # kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
            # '%Y-%m-%dT%H:%M:%S.%f')
            # del kwargs['__class__']
            # self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        new_dict = self.__dict__.copy()
        if '_sa_instance_state' in new_dict.keys():
            del(new_dict['_sa_instance_state'])
        # return '[{}] ({}) {}'.format(type(self).__name__, self.id, new_dict)
        return '[{}] ({}) {}'.format(cls, self.id, new_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        # from models import storage
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()
        # print("Save from basemodel works")

    def to_dict(self):
        "data.drop_all(s""Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del(dictionary['_sa_instance_state'])
        return dictionary

    def delete(self):
        """Deletes the current instance from storage
        Usage:
            obj.delete()
        """

        objs_Dict = storage.all()
        for key, value in objs_Dict.items():
            if self == value:
                del(objs_Dict[key])
                return
