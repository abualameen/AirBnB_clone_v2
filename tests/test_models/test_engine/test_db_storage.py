import unittest
import os
from models import storage
from models.base_model import BaseModel

@unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', 'Test only for DBStorage')
class TestDBStorage(unittest.TestCase):
    """ Class to test the database storage method """
    def setUp(self):
        """ Set up test environment """
        pass

    def tearDown(self):
        """ Remove storage file at the end of tests """
        storage._DBStorage__session.close()
        storage._DBStorage__session.remove()

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    def test_new(self):
        """ New object is correctly added to __objects """
        new = BaseModel()
        storage.new(new)
        storage.save()
        key = '{}.{}'.format(new.__class__.__name__, new.id)
        self.assertIn(key, storage.all())

    def test_all(self):
        """ __objects is properly returned """
        new = BaseModel()
        storage.new(new)
        storage.save()
        temp = storage.all()
        self.assertIsInstance(temp, dict)

    def test_base_model_instantiation(self):
        """ Database is not created on BaseModel save """
        new = BaseModel()
        storage.save()
        self.assertFalse(os.path.exists('file.json'))

    def test_empty(self):
        """ Data is saved to the database """
        new = BaseModel()
        storage.new(new)
        storage.save()
        new2 = BaseModel()
        thing = new.to_dict()
        new2.__dict__.update(thing)
        self.assertNotEqual(len(storage.all()), 0)

    def test_save(self):
        """ DBStorage save method """
        new = BaseModel()
        storage.new(new)
        storage.save()
        self.assertTrue(len(storage.all()) > 0)

    def test_reload(self):
        """ Storage file is successfully loaded to __objects """
        new = BaseModel()
        storage.new(new)
        storage.save()
        storage.reload()
        loaded = storage.all()[new.__class__.__name__ + '.' + new.id]
        self.assertEqual(new.to_dict()['id'], loaded.to_dict()['id'])

    def test_reload_empty(self):
        """ Load from an empty database """
        with self.assertRaises(ValueError):
            storage.reload()

    def test_base_model_save(self):
        """ BaseModel save method calls storage save """
        new = BaseModel()
        new.save()
        self.assertTrue(len(storage.all()) > 0)

    def test_type_path(self):
        """ Confirm __file_path is string """
        self.assertEqual(type(storage._DBStorage__engine), type(None))

    def test_type_objects(self):
        """ Confirm __objects is a dict """
        self.assertEqual(type(storage.all()), dict)

    def test_key_format(self):
        """ Key is properly formatted """
        new = BaseModel()
        storage.new(new)
        storage.save()
        _id = new.id
        key = '{}.{}'.format(new.__class__.__name__, _id)
        self.assertIn(key, storage.all())

    def test_storage_var_created(self):
        """ DBStorage object storage created """
        from models.engine.db_storage import DBStorage
        self.assertEqual(type(storage), DBStorage)


if __name__ == '__main__':
    unittest.main()
 