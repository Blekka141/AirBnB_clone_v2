#!/usr/bin/python
""" Holds class Place """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship

# Define the association table for the Many-to-Many relationship between Place and Amenity
if models.storage_t == 'db':
    place_amenity = Table(
        'place_amenity', Base.metadata,
        Column('place_id', String(60), ForeignKey('places.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True),
        Column('amenity_id', String(60), ForeignKey('amenities.id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    )

class Place(BaseModel, Base):
    """ Representation of Place """
    if models.storage_t == 'db':
        __tablename__ = 'places'
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
        amenities = relationship("Amenity", secondary=place_amenity, back_populates="places", viewonly=False)
        reviews = relationship("Review", backref="place")
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = None
        longitude = None
        amenity_ids = []

    def __init__(self, *args, **kwargs):
        """ Initializes Place """
        super().__init__(*args, **kwargs)
        if models.storage_t != 'db':
            self.city_id = kwargs.get('city_id', "")
            self.user_id = kwargs.get('user_id', "")
            self.name = kwargs.get('name', "")
            self.description = kwargs.get('description', "")
            self.number_rooms = kwargs.get('number_rooms', 0)
            self.number_bathrooms = kwargs.get('number_bathrooms', 0)
            self.max_guest = kwargs.get('max_guest', 0)
            self.price_by_night = kwargs.get('price_by_night', 0)
            self.latitude = kwargs.get('latitude', None)
            self.longitude = kwargs.get('longitude', None)
            self.amenity_ids = []

    if models.storage_t != 'db':
        @property
        def reviews(self):
            """ Getter for list of Review instances """
            from models.review import Review
            return [r for r in models.storage.all(Review).values() if r.place_id == self.id]

        @property
        def amenities(self):
            """ Getter for list of Amenity instances """
            from models.amenity import Amenity
            return [models.storage.all(Amenity)[a_id] for a_id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """ Setter that adds an Amenity.id to the amenity_ids list """
            from models.amenity import Amenity
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
