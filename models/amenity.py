#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    class Amenity(BaseModel, Base):
        
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity")
else:
    class Amenity(BaseModel):
        name = ""