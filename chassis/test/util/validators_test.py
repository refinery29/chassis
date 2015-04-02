"""Test Utility Encoders."""
# pylint: disable=missing-docstring

from chassis import test
from chassis.util import validators


class TestBaseValidator(test.TestCase):

    def test_default_failure(self):
        validator = validators.BaseValidator()
        self.assertRaisesWithMessage(validators.ValidationError,
                                     "Validation failed.",
                                     validator.fail)

    def test_validate_not_implemented(self):
        validator = validators.BaseValidator()
        self.assertRaises(NotImplementedError, validator.validate, 'foo')

    def test_override_message(self):
        new_message = "Foo Message."
        validator = validators.BaseValidator(message=new_message)
        self.assertEqual(validator.get_message(), new_message)
        self.assertRaisesWithMessage(validators.ValidationError,
                                     new_message,
                                     validator.fail)

    def test_default_documentation(self):
        validator = validators.BaseValidator()
        self.assertEqual(validator.get_documentation(), "Validated Parameter.")

    def test_override_documentation(self):
        new_documentation = "Foo Message."
        validator = validators.BaseValidator(documentation=new_documentation)
        self.assertEqual(validator.get_documentation(), new_documentation)


class TestBoolean(test.TestCase):

    def setUp(self):
        self.validator = validators.Boolean()

    def test_true_inputs(self):

        true_values = ('true', 'TRUE', 'True', 'tRUE', 'tRuE', 't', 'T',
                       'yes', 'YES', 'Yes', 'YeS', 'yEs', 'y', 'Y',
                       '1', True, 1)

        for value in true_values:
            self.assertEqual(True, self.validator.validate(value))

    def test_false_inputs(self):

        false_values = ('false', 'FALSE', 'False', 'fALSE', 'fAlSe', 'f', 'F',
                        'no', 'NO', 'No', 'nO', 'n', 'N',
                        '0', False, 0)

        for value in false_values:
            self.assertEqual(False, self.validator.validate(value))

    def test_error_inputs(self):

        error_values = ('foo', '3', 3, None, object(), {}, [1, ], (1, ))

        for value in error_values:
            self.assertRaises(validators.ValidationError,
                              self.validator.validate,
                              value)


class TestString(test.TestCase):

    def test_basic_string(self):
        validator = validators.String()
        self.assertEqual('foo', validator.validate('foo'))

    def test_not_a_string(self):
        validator = validators.String()
        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          42)

    def test_min_length(self):
        validator = validators.String(min_length=3)

        self.assertEqual('foo', validator.validate('foo'))
        self.assertEqual('foobar', validator.validate('foobar'))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          'fo')

    def test_max_length(self):
        validator = validators.String(max_length=4)

        self.assertEqual('foo', validator.validate('foo'))
        self.assertEqual('fooz', validator.validate('fooz'))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          'fooze')

    def test_min_and_max_lengths(self):
        validator = validators.String(min_length=2, max_length=4)

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          'f')

        self.assertEqual('fo', validator.validate('fo'))
        self.assertEqual('foo', validator.validate('foo'))
        self.assertEqual('fooz', validator.validate('fooz'))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          'fooze')


class TestRegex(test.TestCase):

    def setUp(self):
        self.validator = validators.Regex('[a-zA-Z0-9]{2,4}')

    def test_regex_pass(self):
        self.assertEqual('f0', self.validator.validate('f0'))
        self.assertEqual('f00', self.validator.validate('f00'))
        self.assertEqual('f00z', self.validator.validate('f00z'))

    def test_regex_fail(self):

        self.assertRaises(validators.ValidationError,
                          self.validator.validate,
                          'f')

        self.assertRaises(validators.ValidationError,
                          self.validator.validate,
                          'fooze')

        self.assertRaises(validators.ValidationError,
                          self.validator.validate,
                          '***')


class TestInteger(test.TestCase):

    def test_basic_integer(self):
        validator = validators.Integer()
        self.assertEqual(42, validator.validate('42'))
        self.assertEqual(42, validator.validate(42))
        self.assertEqual(0, validator.validate('0'))
        self.assertEqual(-10, validator.validate('-10'))

    def test_not_an_integer(self):
        validator = validators.Integer()

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          31.2)
        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          '42.1')
        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          'foo')
        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          '10-21')

    def test_min_integer(self):
        validator = validators.Integer(minimum=2)
        self.assertEqual(2, validator.validate('2'))
        self.assertEqual(42, validator.validate(42))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          1)

    def test_max_integer(self):
        validator = validators.Integer(maximum=42)
        self.assertEqual(1, validator.validate('1'))
        self.assertEqual(42, validator.validate(42))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          43)

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          10000000)

    def test_min_and_max_integer(self):
        validator = validators.Integer(minimum=2, maximum=42)

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          1)

        self.assertEqual(2, validator.validate('2'))
        self.assertEqual(10, validator.validate('10'))
        self.assertEqual(42, validator.validate(42))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          43)


class TestNumber(test.TestCase):

    def test_basic_number(self):
        validator = validators.Number()
        self.assertEqual(42, validator.validate('42'))
        self.assertEqual(42, validator.validate(42))
        self.assertEqual(0, validator.validate('0'))
        self.assertEqual(-10, validator.validate('-10'))
        self.assertEqual(1.2, validator.validate('1.2'))
        self.assertEqual(-10.345, validator.validate('-10.345'))

    def test_not_a_number(self):
        validator = validators.Number()

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          'foobar')
        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          '10.2.b')
        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          '10*21')

    def test_min_number(self):
        validator = validators.Number(minimum=2.5)

        self.assertEqual(2.5, validator.validate('2.5'))
        self.assertEqual(42, validator.validate(42))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          2.4999)

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          1)

    def test_max_number(self):
        validator = validators.Number(maximum=42.42)

        self.assertEqual(1, validator.validate('1'))
        self.assertEqual(42.42, validator.validate(42.42))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          42.43000001)

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          10000000)

    def test_min_and_max_number(self):
        validator = validators.Number(minimum=2.1, maximum=42.9)

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          2.09)

        self.assertEqual(2.1, validator.validate('2.1'))
        self.assertEqual(10, validator.validate('10'))
        self.assertEqual(42.9, validator.validate(42.9))

        self.assertRaises(validators.ValidationError,
                          validator.validate,
                          42.91)
