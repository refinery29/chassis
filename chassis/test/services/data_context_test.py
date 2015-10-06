import unittest

from chassis.services import data_context
from chassis.test.services.foo_context import FooContext


class UnextendedDatasourceContextTest(unittest.TestCase):
    """Unit test that an unextended DatasourceContext
    methods raise NotImplementedErrors

    """
    def test_insert_raises_error(self):
        """insert should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        with self.assertRaises(NotImplementedError):
            context.insert('query', ['params'])

    def test_get_connection_raises_error(self):
        """_get_connection should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        with self.assertRaises(NotImplementedError):
            context._get_connection()

    def test_close_connection_raises_error(self):
        """_close_connection should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        with self.assertRaises(NotImplementedError):
            context._close_connection()

    def test_enter_raises_error(self):
        """__enter__ should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        with self.assertRaises(NotImplementedError):
            with context as connection:
                self.assertFalse('This statement should not be executed')
