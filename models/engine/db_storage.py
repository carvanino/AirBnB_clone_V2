#!/usr/bin/python3
"""
Strorage engine for database
"""
import models
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.review import Review
from models.amenity import Amenity

"""
from models.base_model import Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
"""


class DBStorage:
    """
    Definition of the class DBStorage
    """

    __engine = None
    __session = None

    def __init__(self):
        """ Initialization of the class with attributes """

        USER = getenv('HBNB_MYSQL_USER')
        PASSWRD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(
                'mysql+mysqldb://{}:{}@{}/{}'
                .format(USER, PASSWRD, HOST, DB), pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session all objects """

        objDict = {}
        if cls is None:
            classes = {
                    'State': State,
                    'City': City,
                    'User': User,
                    'Place': Place,
                    'Review': Review,
                    'Amenity': Amenity}
            for key, value in classes.items():
                # print("Here")
                objct = self.__session.query(value).all()
                for obj in objct:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    # print(key)
                    objDict[key] = obj
        else:
            if type(cls) == str:
                cls = eval(cls)
            objct = self.__session.query(cls)
            for obj in objct:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                objDict[key] = obj

        # print(objDict)
        return objDict

    def new(self, obj):
        """ Adds obj to the current database session """

        # print("new works")
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """

        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes from the current database session obj """

        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Create the current database session from engine"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False)
        # print("reload works")
        self.__session = scoped_session(session_factory)

    def close(self):
        """ Close the current db session """

        # self.__session.remove()
        self.__session.close()
