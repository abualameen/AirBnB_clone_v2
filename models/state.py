#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
import os


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    class State(BaseModel, Base):
        """ State class """
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship(
                                "City", backref="state",
                                cascade="all, delete-orphan")
else:
    class State(BaseModel):
        name = ""

        @property
        def cities(self):
            """
            Getter attribute to return the list
            of the city instances with state_id
            same as the current State.id

            """
            from models import storage
            from models.city import City
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
