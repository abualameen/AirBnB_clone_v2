#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if kwargs:
            print('kwargs', kwargs)
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(
                                        kwargs['created_at'],
                                        '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.created_at = datetime.now()

            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(
                                        kwargs['updated_at'],
                                        '%Y-%m-%dT%H:%M:%S.%f')
            else:
                self.updated_at = datetime.now()

            if '__class__' in kwargs:
                del kwargs['__class__']
            
            import os
            
            # Handle database storage
            if os.getenv('HBNB_TYPE_STORAGE') == 'db':
                for key, value in kwargs.items():
                    if key != '__class__':
                        setattr(self, key, value)
            # Handle file storage
            else:
                for key, value in kwargs.items():
                    setattr(self, key, value)
            # Set the id attribute
            if 'id' not in kwargs:
                self.id = str(uuid.uuid4())

        else:
            #from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # storage.new(self)
    import os

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        # def __str__(self):
        #     """String representation of the State instance"""
        #     cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        #     state_dic = self.__dict__
        #     state_dic.pop('_sa_instance_state', None)
        #     return "[{}] ({}) {}".format(self.__class__.__name__, self.id, {
        #         'name': getattr(self, 'name', ''),
        #         'id': self.id,
        #         'updated_at': self.updated_at,
        #         'created_at': self.created_at
        #     })
        def __str__(self):
            """Returns a string representation of the instance"""
            cls = (str(type(self)).split('.')[-1]).split('\'')[0]
            state_dic = self.__dict__
            state_dic.pop('_sa_instance_state', None)
            return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)
    elif os.getenv('HBNB_TYPE_STORAGE') == 'fs':
        # def __str__(self):
        #     return "[{}] ({}) {}".format(self.__class__.__name__, self.id, {
        #         'name': getattr(self, 'name', ''),
        #         'id': self.id,
        #         'updated_at': self.updated_at,
        #         'created_at': self.created_at
        #     })

        def __str__(self):
            """Returns a string representation of the instance"""
            cls = (str(type(self)).split('.')[-1]).split('\'')[0]
            return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update(
                            {'__class__':
                                (str(type(self))
                                    .split('.')[-1])
                                .split('\'')[0]})
        if isinstance(self.created_at, datetime):
            dictionary['created_at'] = self.created_at.isoformat()
        # else:
        #     dictionary["created_at"] = str(self.created_at)  # Convert to string if not datetime
        if isinstance(self.updated_at, datetime):
            dictionary['updated_at'] = self.updated_at.isoformat()
        # else:
        #     dictionary["updated_at"] = str(self.updated_at) 
        return dictionary

    def delete(self):
        """ delete the current instance from storage """
        storage.delete(self)
