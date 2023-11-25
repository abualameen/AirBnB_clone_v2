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

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Console"
        self.value = HBNBCommand

    def test_create(self):
        """ Test create command """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create BaseModel")
            self.assertNotEqual(outputstd.getvalue(), "")

    def test_create_missing_class(self):
        """ Test create command with missing class name """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create")
            self.assertIn("** class name missing **", outputstd.getvalue())

    def test_create_invalid_class(self):
        """ Test create command with invalid class name """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create InvalidClass")
            self.assertIn("** class doesn't exist **", outputstd.getvalue())

    def test_create_with_name_attribute(self):
        """ Test create command with name attribute """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create State name='California'")
            self.assertIn("California", outputstd.getvalue())

    def test_create_existing_object_with_name(self):
        """ Test create command with existing object and name attribute """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create State name='California'")
            self.value().onecmd("create State name='California'")
            self.assertIn(
                "** object with the same name 'California' already exists"
                " for class 'State' **", outputstd.getvalue())

    def test_create_invalid_name_attribute(self):
        """ Test create command with invalid name attribute """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create State invalid_name='California'")
            self.assertIn(
                "** missing 'name' attribute for class 'State' **",
             outputstd.getvalue())

    def test_create_user_missing_email_password(self):
        """ Test create command with User missing email and password """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create User")
            self.assertIn(
                "** email and password are required for User creation **",
             outputstd.getvalue())

    def test_create_existing_user(self):
        """ Test create command with existing User """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("create User email='test@example.com' password='password'")
            self.value().onecmd("create User email='test@example.com' password='password'")
            self.assertIn(
                "** User with the same email 'test@example.com' already exists **",
             outputstd.getvalue())

    def test_all(self):
        """ Test all command """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("all")
            self.assertNotEqual(outputstd.getvalue(), "")

    def test_all_with_class(self):
        """ Test all command with class """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("all BaseModel")
            self.assertNotEqual(outputstd.getvalue(), "")

    def test_all_invalid_class(self):
        """ Test all command with invalid class """
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as outputstd:
            self.value().onecmd("all InvalidClass")
            self.assertIn("** class doesn't exist **", outputstd.getvalue())


if __name__ == "__main__":
    unittest.main()

