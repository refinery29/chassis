"""Chassis Base Test Case."""

import unittest


class TestCase(unittest.TestCase):
    """Base test case with chassis-specific extensions."""

    # pylint: disable=invalid-name
    def assertRaisesWithMessage(self, exception_type, message, func,
                                *args, **kwargs):
        """Assert that executing func with the provided arguments raise the
        given exception with the given message string."""

        try:
            func(*args, **kwargs)
        except exception_type as err:
            self.assertEqual(err.args[0], message)
        else:
            self.fail('"{0}" was expected to throw "{1}" exception'
                      .format(func.__name__, exception_type.__name__))
