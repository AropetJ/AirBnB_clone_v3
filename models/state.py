#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
import os
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')


class State(BaseModel, Base):
    """Representation of state """
    if STORAGE_TYPE == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

        @property
        def cities(self):
            """
                getter method, returns list of City objs from storage
                linked to the current State
            """
            city_list = []
            for city in models.storage.all("City").values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
