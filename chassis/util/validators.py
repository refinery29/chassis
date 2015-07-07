"""Parameter Parsing and Validation for Chassis Applications."""

import re
import six


class ValidationError(Exception):
    """Raised when validation fails."""


class BaseValidator(object):
    """Base class for validators."""

    def __init__(self):
        self.documentation = "Validated Parameter."
        self.message = "Validation failed."

    def fail(self):
        """Raise a validation error with the messsage."""
        raise ValidationError(self.message)

    def validate(self, unused_value, unused_handler):
        """Override this to implement validation logic.

        Return the validated value or call self.fail() to raise a
        ValidationError.
        """
        raise NotImplementedError


class Boolean(BaseValidator):
    """Validates Boolean inputs for truthiness."""

    truthy = ['true', '1', 'yes', 't', 'y', True, 1]
    falsy = ['false', '0', 'no', 'f', 'n', False, 0]

    def __init__(self):
        super(Boolean, self).__init__()
        self.documentation = "Truthy value: Prefered `true` or `false`"
        self.message = "Valid boolean required"

    def validate(self, value, unused_handler):
        if isinstance(value, six.string_types):
            value = value.lower()

        if value in self.truthy:
            return True

        if value in self.falsy:
            return False

        self.fail()


class String(BaseValidator):
    """Validates strings with optional length requirements."""


    def __init__(self, min_length=None, max_length=None):
        super(String, self).__init__()

        # TODO: Overwrite self.message based on parameters.
        self.documentation = "String."
        self.message = "Valid string required."
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, value, unused_handler):
        if not isinstance(value, six.string_types):
            self.fail()

        length = len(value)

        if self.min_length is not None:
            if length < self.min_length:
                self.fail()

        if self.max_length is not None:
            if length > self.max_length:
                self.fail()

        return value


class Regex(BaseValidator):
    """Validates a string agains a regular expression."""


    def __init__(self, regex):
        super(Regex, self).__init__()
        self.documentation = "Regex."
        self.message = "String matching regular expression required."
        self.pattern = re.compile(regex)

    def validate(self, value, unused_handler):
        match = self.pattern.match(value)

        if match and value == match.group():
            return value

        self.fail()


class Number(BaseValidator):
    """Validates floating point numbers with optional length requirements."""

    def __init__(self, minimum=None, maximum=None):
        super(Number, self).__init__()
        self.documentation = "Number."
        self.message = "Valid number required."
        self.minimum = minimum
        self.maximum = maximum


    def validate(self, value, unused_handler):
        try:
            value = float(value)
        except ValueError:
            self.fail()

        if self.minimum is not None and value < self.minimum:
            self.fail()

        if self.maximum is not None and value > self.maximum:
            self.fail()

        return value


class Integer(Number):
    """Validates integers with optional length requirements."""

    def __init__(self, minimum=None, maximum=None):
        super(Integer, self).__init__(minimum=minimum, maximum=maximum)
        self.documentation = "Integer."
        self.message = "Valid integer required."

    def validate(self, value, handler):

        # Do the Number validation first
        float_value = super(Integer, self).validate(value, handler)

        int_value = int(float_value)

        if int_value == float_value:
            return int_value
        else:
            self.fail()
