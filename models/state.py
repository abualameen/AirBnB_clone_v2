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
        cities = relationship("City", backref="state", cascade="all, delete-orphan")

        # def __str__(self):
        #     """String representation of the State instance"""
        #     # Exclude _sa_instance_state and __class__ from the string representation
        #     state_dict = self.to_dict()
        #     state_dict.pop('_sa_instance_state', None)
        #     state_dict.pop('__class__', None)
        #     return "[{}] ({}) {}".format(self.__class__.__name__, self.id, state_dict)
        
else:
    class State(BaseModel):
        name = ""

        @property
        def cities(self):
            """
            Getter attribute to return the list of the city instances with state_id
            same as the current State.id

            """
            from models import storage
            cities_list = []
            for city in storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list