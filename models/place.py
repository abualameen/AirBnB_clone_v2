#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel
from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String
from sqlalchemy import DateTime, ForeignKey, Float, Table
from sqlalchemy.orm import relationship
import os


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    class Place(BaseModel, Base):
        """ A place to stay """
        __tablename__ = 'places'
        place_amenity = Table(
                                "place_amenity", Base.metadata,
                                Column(
                                        "place_id", String(60),
                                        ForeignKey("places.id"),
                                        primary_key=True, nullable=False),
                                Column(
                                        "amenity_id", String(60),
                                        ForeignKey("amenities.id"),
                                        primary_key=True, nullable=False))
        amenities = relationship(
                                    "Amenity", secondary=place_amenity,
                                    back_populates="place_amenities",
                                    viewonly=False)
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship(
                                'Review', backref='place',
                                cascade='all, delete-orphan')

else:
    class Place(BaseModel):
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            Getter attribute that returns the list of Review instances
            with place_id equals to the current Place.id
            """
            from models import storage
            reviews_list = []
            all_reviews = storage.all(Review)
            for review in all_reviews.values():
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """ Getter attribute amenities that returns the list of Amenity
            instances based on the attribute amenity_ids that contains all
            Amenity.id linked to the Place """
            amenity_objs = models.storage.all(Amenity)
            return [amenity for amenity in amenity_objs.values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, amenity):
            """ Setter attribute amenities that handles append method
            for adding an Amenity.id to the attribute amenity_ids.
            This method should accept only Amenity
            object, otherwise, do nothing. """
            if isinstance(amenity, Amenity):
                self.amenity_ids.append(amenity.id)
