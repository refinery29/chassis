"""Unit test for chassis.services.data_context module"""
# pylint: disable=invalid-name, protected-access
import unittest

from chassis.services import data_context


class UnextendedDatasourceContextTest(unittest.TestCase):
    """Unit test that an unextended DatasourceContext
    methods raise NotImplementedErrors

    """
    def test_insert_raises_error(self):
        """insert should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        self.assertRaises(NotImplementedError, context.insert, 'query',
                          ['params'])

    def test_get_connection_raises_error(self):
        """_get_connection should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        self.assertRaises(NotImplementedError, context._get_connection)

    def test_close_connection_raises_error(self):
        """_close_connection should raise a NotImplementedError"""
        context = data_context.DatasourceContext()
        self.assertRaises(NotImplementedError, context._close_connection)

    def test_enter_raises_error(self):
        """__enter__ should raise a NotImplementedError"""
        # pylint: disable=unused-variable, redundant-unittest-assert
        context = data_context.DatasourceContext()
        self.assertRaises(NotImplementedError, context.__enter__)
