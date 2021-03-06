"""Utility Parameter Tools for Chassis Applications."""

import six
from tornado import web

from chassis.util import decorators
from chassis.util import validators


def _fetch_arguments(handler, method):
    """Get the arguments depending on the type of HTTP method."""

    if method.__name__ == 'get':
        arguments = {}
        for key, value in six.iteritems(handler.request.arguments):
            # Tornado supports comma-separated lists of values in
            # parameters. We're undoing that here, and if a list
            # is expected the _validate method can handle it.
            if isinstance(value, list):
                arguments[key] = ','.join(value)
            else:
                arguments[key] = value
    else:  # post, put, patch, delete?
        arguments = handler.get_post_arguments()

    return arguments


def _apply_validator_chain(chain, value, handler):
    """Apply validators in sequence to a value."""

    if hasattr(chain, 'validate'):  # not a list
        chain = [chain, ]

    for validator in chain:
        if hasattr(validator, 'validate'):
            value = validator.validate(value, handler)
        else:
            raise web.HTTPError(500)
    return value


def _parse_arguments(self, method, parameters):
    """Parse arguments to method, returning a dictionary."""

    # TODO: Consider raising an exception if there are extra arguments.

    arguments = _fetch_arguments(self, method)

    arg_dict = {}
    errors = []
    for key, properties in parameters:
        if key in arguments:
            value = arguments[key]
            try:
                arg_dict[key] = _apply_validator_chain(
                    properties.get('validators', []), value, self)
            except validators.ValidationError as err:
                errors.append(err)
        else:
            if properties.get('required', False):
                raise web.HTTPError(
                    400,
                    ('Missing required parameter: %s'
                     % (key, ))
                    )
            else:
                if properties.get('default', None) is not None:
                    arg_dict[key] = properties['default']
                else:
                    arg_dict[key] = None
    if errors:
        raise web.HTTPError(400, 'There were %s errors' % len(errors))

    return arg_dict


def parse(parameters):
    """Decorator to parse parameters according to a set of criteria.

    This outer method is called to set up the decorator.

    Arguments:
        parameters: An array of parameter declarations tuples in the format:
        ('<param_name>', {'validate': [<ValidatorClass>,...], <options...>})

    Usage:

    @chassis.util.parameters.parse([
        ('email', {'validators': [validators.Email], 'required': True}),
        ('password', {'validators': [validators.Password], 'required': True})
        ])
    def post(self, email=None, password=None):
        # Render JSON for the provided parameters
        self.render_json({'email': email, 'password': password})
    """
    # pylint: disable=protected-access
    @decorators.include_original
    def decorate(method):
        """Setup returns this decorator, which is called on the method."""

        def call(self, *args):
            """This is called whenever the decorated method is invoked."""

            kwargs = _parse_arguments(self, method, parameters)
            return method(self, *args, **kwargs)

        # TODO: Autogenerate documentation data for parameters.

        return call
    return decorate


def parse_dict(parameters):
    """Decorator to parse parameters as a dict according to a set of criteria.

    This outer method is called to set up the decorator.

    Arguments:
        parameters: An array of parameter declarations tuples in the format:
        ('<param_name>', {'validate': [<ValidatorClass>,...], <options...>})

    Usage:

    @chassis.util.parameters.parse_dict([
        ('email', {'validators': [validators.Email], 'required': True}),
        ('password', {'validators': [validators.Password], 'required': True})
        ])
    def post(self, data):
        # Render JSON for the provided parameters
        self.render_json({'email': data['email'],
                          'password': data['password']})
    """
    # pylint: disable=protected-access
    @decorators.include_original
    def decorate(method):
        """Setup returns this decorator, which is called on the method."""

        def call(self, *args):
            """This is called whenever the decorated method is invoked."""

            arg_dict = _parse_arguments(self, method, parameters)
            return method(self, *args, data=arg_dict)

        # TODO: Autogenerate documentation data for parameters.

        return call
    return decorate
