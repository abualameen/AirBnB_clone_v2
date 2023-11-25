#!/usr/bin/python3
"""
this module handles interactions with the mysql data base
using SQLALchemy

"""
from models.base_model import Base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    """ this class handles interaction with mysql data base """
    __engine = None
    __session = None
    __objects = {}

    def __init__(self):
        """ initialize the DBStoragae instances """
        db_user = os.environ.get('HBNB_MYSQL_USER')
        db_password = os.environ.get('HBNB_MYSQL_PWD')
        db_host = os.environ.get('HBNB_MYSQL_HOST')
        db_name = os.environ.get('HBNB_MYSQL_DB')

        self.__engine = create_engine(
                                        f'mysql+mysqldb://{db_user}:{db_password}\
                                        @{db_host}/{db_name}',
                                        pool_pre_ping=True)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))
        if os.environ.get('HBNB_ENV') == 'test':
            Base.metatdata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
        else:
            classes = [cls]

        objects = self.__objects
        for cls in classes:
            if issubclass(cls, BaseModel):
                try:
                    query_result = self.__session.query(cls).all()
                    for obj in query_result:
                        key = f"{type(obj).__name__}.{obj.id}"
                        obj_dict = obj.to_dict()
                        objects[key] = f"[{type(obj).__name__}]\
                                        ({obj.id}) {obj_dict}"
                except Exception as e:
                    print(f"Error querying {cls}: {e}")
        return objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Saves storage database to file"""
        try:
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def reload(self):
        """Loads storage dictionary from db"""
        from models.base_model import BaseModel
        from models.state import State
        from models.city import City
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity

        classes = {
                    State, City, User, Place, Review, Amenity

                  }
        Base.metadata.create_all(self.__engine)
        self.__session.remove()
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
        for cls in classes:
            table_name = cls.__tablename__  # Get the table name
            query_result = self.__session.query(cls).all()
            for obj in query_result:
                key = f"{type(obj).__name__}.{obj.id}"
                self.__objects[key] = obj

    def delete(self, obj=None):
        """ this methed delets object of a given class """
        if obj is not None:
            try:
                self.__session.delete(obj)
                self.save()
            except Exception as e:
                pass
