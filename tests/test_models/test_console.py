from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
import unittest
from models import storage
from datetime import datetime
import unittest
import models
from models.base_model import BaseModel
from models.state import State


class TestConsole(unittest.TestCase):
    """ Test the console """
    def test_created_at(self):
        """ Test created_at attribute """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
        instance_id = output
        obj = models.storage.all().get(f"BaseModel.{instance_id}")
        self.assertIs(type(obj.created_at), datetime)

    def test_id(self):
        """ Test id attribute """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
        instance_id = output
        self.assertIs(type(instance_id ), str)

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
        self.assertIn('HBNBCommand', str(HBNBCommand()))

    def test_todict(self):
        """ Test to_dict method """
        with self.assertRaises(AttributeError):
            HBNBCommand().to_dict()

    def test_updated_at(self):
        """ Test updated_at attribute """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create BaseModel")
            output = f.getvalue().strip()
        instance_id = output
        obj = models.storage.all().get(f"BaseModel.{instance_id}")
        self.assertIs(type(obj.updated_at), datetime)


if __name__ == '__main__':
    unittest.main()
