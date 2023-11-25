#!/usr/bin/python3
""" """
import unittest
from tests.test_models.test_base_model import test_basemodel
from console import HBNBCommand
import io
import unittest.mock
from models import storage


class test_Console(test_basemodel):
    """ """
    def test_created_at(self):
        """ Test created_at attribute """
        self.assertIs(type(HBNBCommand().created_at), datetime.datetime)

    def test_id(self):
        """ Test id attribute """
        self.assertIs(type(HBNBCommand().id), str)

    def test_kwargs(self):
        """ Test passing kwargs """
        with self.assertRaises(TypeError):
            HBNBCommand(**{"Name": "John"})

    def test_kwargs_int(self):
        """ Test passing kwargs with int """
        with self.assertRaises(TypeError):
            HBNBCommand(**{"age": 25})

    def test_kwargs_one(self):
        """ Test passing one unexpected kwargs """
        with self.assertRaises(TypeError):
            HBNBCommand(**{"Name": "John", "age": 25})

    def test_save(self):
        """ Testing save method """
        with self.assertRaises(AttributeError):
            HBNBCommand().save()

    def test_str(self):
        """ Test __str__ method """
        self.assertIn('[HBNBCommand]', str(HBNBCommand()))

    def test_todict(self):
        """ Test to_dict method """
        with self.assertRaises(AttributeError):
            HBNBCommand().to_dict()

    def test_updated_at(self):
        """ Test updated_at attribute """
        self.assertIs(type(HBNBCommand().updated_at), datetime.datetime)


if __name__ == '__main__':
    unittest.main()
