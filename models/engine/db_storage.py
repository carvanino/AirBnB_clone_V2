#!/usr/bin/python3
"""
Strorage engine for database
"""
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
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
from os import getenv




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
        if cls == None:
            classes = {'User': User, 'State': State, 'City': City, 'Amenity': Amenity}
            for key, value in classes.items():
                print("Here")
                objct = self.__session.query(value)
                print(obj)
                for obj in objct:
                    print("obj")
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objDict[key] = obj
        else:
            objct = self.__session.query(cls)
            key = "{}.{}".format(type(obj).__name__, obj.id)
            objDict[key] = obj

        return objDict

    def new(self, obj):
        """ Adds obj to the current database session """

        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """

        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes from the current database session obj """

        if obj == None:
            self.__session.delete(obj)

    def reload(self):
        """ Create the current database session from engine"""

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, 
                expire_on_commit=False)
        self.__session = scoped_session(session_factory)
