"""Unit Test for cache.services.cache module"""
# pylint: disable=invalid-name
import unittest
import yaml

from chassis.services import cache


def get_config_yaml():
    """Load Test Config"""
    config_file = open('./test/test_config.yml', 'r')
    return yaml.load(config_file) or {}


class CacheTest(unittest.TestCase):
    """Cache Unit Test"""
    _config = None

    _cache = None

    def setUp(self):
        """Create Redis"""
        if self._config is None:
            self._config = get_config_yaml()

        self._cache = cache.Cache(self._config['redis'])

    def tearDown(self):
        """Flush Database"""
        with self._cache as redis_connection:
            redis_connection.flushdb()

    def test_set_retrieve_and_delete_object(self):
        """Test set_object, retrieve_object, and delete_object methods"""
        template = {'username': 'user:%(id)s:username',
                    'email': 'user:%(id)s:email',
                    'phone': 'phone:%(id)s:phone'}
        indexes = {'id': 12345}
        data = {'username': 'Bob',
                'email': 'bob@example.com',
                'phone': '555-555-5555'}

        cache.set_object(self._cache, template, indexes, data)

        result = cache.retrieve_object(self._cache, template, indexes)
        self.assertEqual(
            {'username': b'Bob',
             'email': b'bob@example.com',
             'phone': b'555-555-5555'},
            result
            )

        cache.delete_object(self._cache, template, indexes)

        result = cache.retrieve_object(self._cache, template, indexes)
        self.assertEqual(None, result)

    def test_multi_get(self):
        """Test Getting Multipile Keys"""
        templates = {
            'username': 'user:%(id)s:username'
        }
        cache.set_object(self._cache, templates, {'id': 12345},
                         {'username': 'Bob'})
        cache.set_object(self._cache, templates, {'id': 67890},
                         {'username': 'John'})

        result = cache.multi_get(self._cache, ['user:12345:username',
                                               'user:67890:username'])

        self.assertEquals([b'Bob', b'John'], result)

    def test_set_get_and_delete_value(self):
        """Test setting, getting, and deleting value by key"""
        cache.set_object(self._cache,
                         {'username': 'user:%(id)s:username'},
                         {'id': 12345},
                         {'username': 'Bob'})

        cache.set_value(self._cache, 'user:12345:username', 'Harry')

        result = cache.get_value(self._cache, 'user:12345:username')
        self.assertEquals(b'Harry', result)

        result = cache.delete_value(self._cache, 'user:12345:username')
        self.assertEquals(1, result)

        result = cache.get_value(self._cache, 'user:12345:username')
        self.assertEqual(None, result)
