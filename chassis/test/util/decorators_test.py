"""Test Utility Decorators."""
# pylint: disable=missing-docstring

import unittest

from chassis.util import decorators


class TestDecorators(unittest.TestCase):

    def test_include_original(self):

        # Create a test decorator to decorate.
        @decorators.include_original
        def foo_decorator(method):
            def wrapper():
                return method() + "bazbat"
            return wrapper

        # Apply our test decorator to a test method
        @foo_decorator
        def foo_method():
            return 'bar'

        # Assert that the test decorator was applied to the method, resulting
        # in an altered output
        self.assertEquals(foo_method(), 'barbazbat')

        # Assert that the include_original behavior was added to the decorator,
        # resulting in ._original pointing to the original method.
        # pylint: disable=protected-access
        self.assertEquals(foo_method._original(), 'bar')
        self.assertEquals(foo_method._original.__name__, 'foo_method')
