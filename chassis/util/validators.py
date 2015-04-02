"""Parameter Parsing and Validation for Chassis Applications."""

import re
import six


class ValidationError(Exception):
    """Raised when validation fails."""


class BaseValidator(object):
    """Base class for validators."""

    documentation = "Validated Parameter."
    message = "Validation failed."

    def __init__(self, message=None, documentation=None):
        self.override_message = message
        self.override_documentation = documentation

    def get_documentation(self):
        """Retrieve the overridden or default documentation string."""

        if self.override_documentation:
            return self.override_documentation
        else:
            return self.documentation

    def get_message(self):
        """Retrieve the overridden or default error message string."""

        if self.override_message:
            return self.override_message
        else:
            return self.message

    def fail(self):
        """Raise a validation error with the messsage."""

        raise ValidationError(self.get_message())

    def validate(self, unused_value):
        """Override this to implement validation logic.

        Return the validated value or call self.fail() to raise a
        ValidationError.
        """
        raise NotImplementedError


class Boolean(BaseValidator):
    """Validates Boolean inputs for truthiness."""

    truthy = ['true', '1', 'yes', 't', 'y', True, 1]
    falsy = ['false', '0', 'no', 'f', 'n', False, 0]

    documentation = "Truthy value: Prefered `true` or `false`"
    message = "Valid boolean required"

    def validate(self, value):
        if isinstance(value, six.string_types):
            value = value.lower()

        if value in self.truthy:
            return True

        if value in self.falsy:
            return False

        self.fail()


class String(BaseValidator):
    """Validates strings with optional length requirements."""

    documentation = "String."
    message = "Valid string required."

    def __init__(self, min_length=None, max_length=None,
                 message=None, documentation=None):
        self.min_length = min_length
        self.max_length = max_length

        # TODO: Make custom messages based on parameters.

        super(String, self).__init__(message=message,
                                     documentation=documentation)

    def validate(self, value):
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

    documentation = "Regex."
    message = "String matching regular expression required."

    def __init__(self, regex, message=None, documentation=None):
        self.pattern = re.compile(regex)

        super(Regex, self).__init__(message=message,
                                    documentation=documentation)

    def validate(self, value):
        match = self.pattern.match(value)

        if match and value == match.group():
            return value

        self.fail()


class Number(BaseValidator):
    """Validates floating point numbers with optional length requirements."""

    documentation = "Number."
    message = "Valid number required."

    def __init__(self, minimum=None, maximum=None,
                 message=None, documentation=None):

        self.minimum = minimum
        self.maximum = maximum

        super(Number, self).__init__(message=message,
                                     documentation=documentation)

    def validate(self, value):
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

    documentation = "Integer."
    message = "Valid integer required."

    def __init__(self, minimum=None, maximum=None,
                 message=None, documentation=None):

        super(Integer, self).__init__(minimum=minimum, maximum=maximum,
                                      message=message,
                                      documentation=documentation)

    def validate(self, value):

        # Do the Number validation first
        float_value = super(Integer, self).validate(value)

        int_value = int(float_value)

        if int_value == float_value:
            return int_value
        else:
            self.fail()
