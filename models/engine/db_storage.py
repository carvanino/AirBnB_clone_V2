#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from models.base_model import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """This class manages database session of hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """class initialision"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}:3306/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        classes = [
            State, City, Place, Amenity, Review, User]

        rows = []

        if cls:
            rows = self.__session.query(cls)
        else:
            for clss in classes:
                rows += self.__session.query(clss)
        return {type(v).__name__ + "." + v.id: v for v in rows}

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete an object from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))
