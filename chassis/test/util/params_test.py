"""Test Parameter Parser."""
# pylint: disable=missing-docstring

import mock
import unittest
from tornado import web

from chassis.util import params


class TestParamParser(unittest.TestCase):

    def setUp(self):
        self.handler = mock.Mock()
        self.handler.request = mock.Mock()
        self.handler.request.arguments = {}

        self.get = mock.Mock()
        self.get.__name__ = "get"

        self.bar_validator = mock.Mock()
        self.bar_validator.validate = mock.Mock(return_value='bar')

        self.bat_validator = mock.Mock()
        self.bat_validator.validate = mock.Mock(return_value='bat')

        self.baz_validator = mock.Mock()
        self.baz_validator.validate = mock.Mock(return_value='baz')

        self.fail_validator = mock.Mock()
        self.fail_validator.validate = mock.Mock(
            side_effect=web.HTTPError(400))

    def test_optional_parameter(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {'validators': self.bar_validator, 'required': False})
            ])(self.get)

        # Called without parameters, raises an exception
        get(self.handler)
        self.get.assert_called_with(self.handler, foo=None)

        # Called with parameters, returns validated parameter
        self.handler.request.arguments['foo'] = 'Foobar'
        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.get.assert_called_with(self.handler, foo='bar')

    def test_default_parameter(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {
                'validators': self.bar_validator,
                'required': False,
                'default': 42
                })])(self.get)

        # Called without parameters, uses default value
        get(self.handler)
        self.get.assert_called_with(self.handler, foo=42)

        # Called with parameters, returns validated parameter
        self.handler.request.arguments['foo'] = 'Foobar'
        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.get.assert_called_with(self.handler, foo='bar')

    def test_required_parameter(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {'validators': [self.bar_validator], 'required': True})
            ])(self.get)

        # Called without parameters, raises an exception
        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

        # Called with parameters, returns validated parameter
        self.handler.request.arguments['foo'] = 'Foobar'
        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.get.assert_called_with(self.handler, foo='bar')

    def test_failing_parameter(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {'validators': [self.fail_validator], 'required': True})
            ])(self.get)

        # Called without parameters, raises an exception
        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

        # Called with parameters, raises an exception
        self.handler.request.arguments['foo'] = 'Foobar'
        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

    def test_multiple_parameter(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {'validators': self.bar_validator, 'required': True}),
            ('spam', {'validators': self.bat_validator, 'required': True}),
            ('eggs', {'validators': self.baz_validator, 'required': False})
            ])(self.get)

        # Called without parameters, raises an exception
        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

        # Called with required parameters, returns validated parameters
        self.handler.request.arguments['foo'] = 'Foobar'
        self.handler.request.arguments['spam'] = 'Canned Meat'

        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.bat_validator.validate.assert_called_with('Canned Meat')
        self.get.assert_called_with(self.handler,
                                    foo='bar',
                                    spam='bat',
                                    eggs=None)

        # Called with all parameters, returns validated parameters
        self.handler.request.arguments['foo'] = 'Foobar'
        self.handler.request.arguments['spam'] = 'Canned Meat'
        self.handler.request.arguments['eggs'] = 'Over Easy'

        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.bat_validator.validate.assert_called_with('Canned Meat')
        self.get.assert_called_with(self.handler,
                                    foo='bar',
                                    spam='bat',
                                    eggs='baz')

    def test_extra_parameters(self):
        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {'validators': self.bar_validator, 'required': True})
            ])(self.get)

        # Called without parameters, raises an exception
        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

        # Called with extra parameters, trims extra validated parameter
        self.handler.request.arguments['foo'] = 'Foobar'
        self.handler.request.arguments['extra'] = 'Do Not Want'
        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.get.assert_called_with(self.handler, foo='bar')

    def test_chained_validators(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {
                'validators': [self.bar_validator,
                               self.bat_validator,
                               self.baz_validator],
                'required': True
                })])(self.get)

        # Called without parameters, raises an exception

        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

        # Called with parameters, verifies that parameter is passed through
        # each validator in order.

        self.handler.request.arguments['foo'] = 'Foobar'
        get(self.handler)

        self.bar_validator.validate.assert_called_with('Foobar')
        self.bat_validator.validate.assert_called_with('bar')
        self.baz_validator.validate.assert_called_with('bat')

        self.get.assert_called_with(self.handler, foo='baz')

    def test_chained_validators_fail(self):

        # Apply the decorator we're testing to the mock get method
        get = params.parse([
            ('foo', {
                'validators': [self.bar_validator,
                               self.bat_validator,
                               self.fail_validator],
                'required': True
                })])(self.get)

        # Called without parameters, raises an exception

        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)

        # Called with parameters, raises an exception

        self.handler.request.arguments['foo'] = 'Foobar'
        self.assertRaises(web.HTTPError,
                          get,
                          self.handler)
