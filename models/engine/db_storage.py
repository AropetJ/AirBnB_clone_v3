#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user
import os
import sqlalchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """interaacts with the MySQL database"""
    CNC = {
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    __engine = None
    __session = None 

    def __init__(self):
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        obj_dict = {}
        if cls is not None:
            a_query = self.__session.query(DBStorage.CNC[cls])
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
            return obj_dict

        for c in DBStorage.CNC.values():
            a_query = self.__session.query(c)
            for obj in a_query:
                obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[obj_ref] = obj
        return obj_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
            retrieves one object based on class name and id
        """
        if cls and id:
            fetch = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch)
        return None

    def count(self, cls=None):
        """
            returns the count of all objects in storage
        """
        return (len(self.all(cls)))
