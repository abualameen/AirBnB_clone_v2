#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
# models/__init__.py

from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.base_model import BaseModel


__all__ = ['State', 'City', 'User', 'Place', 'Amenity', 'Review', 'BaseModel', 'storage']

import os

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
    from models import storage
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
    


