""" Services Module """

from six import string_types, iteritems


class InvalidServiceConfiguration(Exception):
    """Raised when a service configuration is Invalid"""


class UninstantiatedServiceException(Exception):
    """
        Raised when a service dependency fullfillment
        is attempted before it has been instantiated.
    """


def is_arg_scalar(arg):
    """ Returns true if arg starts with a dollar sign """
    return arg[:1] == '$'


def is_arg_service(arg):
    """ Returns true if arg starts with an at symbol """
    return arg[:1] == '@'


def _check_type(name, obj, expected_type):
    """ Raise a TypeError if object is not of expected type """
    if not isinstance(obj, expected_type):
        raise TypeError(
            '"%s" must be an a %s' % (name, expected_type.__name__)
        )


def _import_module(module_name):
    """
        Imports the module dynamically

        _import_module('foo.bar') calls:
            __import__('foo.bar',
                       globals(),
                       locals(),
                       ['bar', ],
                       0)
    """
    fromlist = []
    dot_position = module_name.rfind('.')
    if dot_position > -1:
        fromlist.append(
            module_name[dot_position+1:len(module_name)]
        )

    # Import module
    module = __import__(module_name, globals(), locals(), fromlist, 0)

    return module


def _verify_create_args(module_name, class_name, static):
    """ Verifies a subset of the arguments to create() """
    # Verify module name is provided
    if module_name is None:
        raise InvalidServiceConfiguration(
            'Service configurations must define a module'
        )

    # Non-static services must define a class
    if not static and class_name is None:
        tmpl0 = 'Non-static service configurations must define a class: '
        tmpl1 = 'module is %s'
        raise InvalidServiceConfiguration((tmpl0 + tmpl1) % module_name)


class ServiceFactory(object):
    """
        Class ServiceFactory handles the dynamic creation of service objects
    """
    def __init__(self, scalars=None):
        if scalars is None:
            self.scalars = {}
        else:
            self.scalars = scalars
        self.instantiated_services = {}

    # pylint: disable=too-many-locals, too-many-arguments
    def create(self, module_name, class_name,
               args=None, kwargs=None, factory_method=None,
               factory_args=None, factory_kwargs=None, static=False,
               calls=None):
        """ Initializes an instance of the service """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if factory_args is None:
            factory_args = []
        if factory_kwargs is None:
            factory_kwargs = {}
        if static is None:
            static = False

        # Verify
        _verify_create_args(module_name, class_name, static)

        # Import
        module = _import_module(module_name)

        # Instantiate
        service_obj = self._instantiate(module, class_name,
                                        args, kwargs, static)
        # Factory?
        if factory_method is not None:
            service_obj = self._handle_factory_method(service_obj,
                                                      factory_method,
                                                      factory_args,
                                                      factory_kwargs)
        # Extra Calls
        if calls is not None and isinstance(calls, list):
            self._handle_calls(service_obj, calls)

        # Return
        return service_obj

    def create_from_dict(self, dictionary):
        """ Initializes an instance from a dictionary blueprint """
        # Defaults
        args = []
        kwargs = {}
        factory_method = None
        factory_args = []
        factory_kwargs = {}
        static = False
        calls = None

        # Check dictionary for arguments
        if 'args' in dictionary:
            args = dictionary['args']

        if 'kwargs' in dictionary:
            kwargs = dictionary['kwargs']

        if 'factory-method' in dictionary:
            factory_method = dictionary['factory-method']

        if 'factory-args' in dictionary:
            factory_args =dictionary['factory-args']

        if 'factory-kwargs' in dictionary:
            factory_kwargs =dictionary['factory-kwargs']

        if 'static' in dictionary:
            static = dictionary['static']

        if 'calls' in dictionary:
            calls = dictionary['calls']

        return self.create(
            dictionary['module'],
            dictionary['class'],
            args=args,
            kwargs=kwargs,
            factory_method=factory_method,
            factory_args=factory_args,
            factory_kwargs=factory_kwargs,
            static=static,
            calls=calls
        )

    def add_instantiated_service(self, name, service):
        """ Add an instatiated service by name """
        self.instantiated_services[name] = service

    def get_instantiated_services(self):
        """ Get instantiated services """
        return self.instantiated_services

    def get_instantiated_service(self, name):
        """ Get instantiated service by name """
        if name not in self.instantiated_services:
            raise UninstantiatedServiceException
        return self.instantiated_services[name]

    def _replace_service_arg(self, name, index, args):
        """ Replace index in list with service """
        args[index] = self.get_instantiated_service(name)

    def _replace_service_kwarg(self, key, kwarg):
        """ Replace key in dictionary with service """
        kwarg[key] = self.get_instantiated_service(key)

    def _replace_scalars_in_args(self, args):
        """ Replace scalars in arguments list """
        _check_type('args', args, list)
        new_args = []
        for arg in args:
            if isinstance(arg, list):
                to_append = self._replace_scalars_in_args(arg)
            elif isinstance(arg, dict):
                to_append = self._replace_scalars_in_kwargs(arg)
            elif isinstance(arg, string_types):
                to_append = self._replace_scalar(arg)
            else:
                to_append = arg
            new_args.append(to_append)
        return new_args

    def _replace_scalars_in_kwargs(self, kwargs):
        """ Replace scalars in keyed arguments dictionary """
        _check_type('kwargs', kwargs, dict)

        new_kwargs = {}
        for (name, value) in iteritems(kwargs):
            if isinstance(value, list):
                new_kwargs[name] = self._replace_scalars_in_args(value)
            elif isinstance(value, dict):
                new_kwargs[name] = self._replace_scalars_in_kwargs(value)
            elif isinstance(value, string_types):
                new_kwargs[name] = self._replace_scalar(value)
            else:
                new_kwargs[name] = value
        return new_kwargs

    def _replace_services_in_args(self, args):
        """ Replace service references in arguments list """
        _check_type('args', args, list)

        new_args = []
        for arg in args:
            if isinstance(arg, list):
                new_args.append(self._replace_services_in_args(arg))
            elif isinstance(arg, dict):
                new_args.append(self._replace_services_in_kwargs(arg))
            elif isinstance(arg, string_types):
                new_args.append(self._replace_service(arg))
            else:
                new_args.append(arg)
        return new_args

    def _replace_services_in_kwargs(self, kwargs):
        """ Replace service references in keyed arguments dictionary """
        _check_type('kwargs', kwargs, dict)

        new_kwargs = {}
        for (name, value) in iteritems(kwargs):
            if isinstance(value, list):
                new_kwargs[name] = self._replace_services_in_args(value)
            elif isinstance(value, dict):
                new_kwargs[name] = self._replace_services_in_kwargs(value)
            elif isinstance(value, string_types):
                new_kwargs[name] = self._replace_service(value)
            else:
                new_kwargs[name] = value
        return new_kwargs

    def get_scalar_value(self, name):
        """ Get scalar value by name """
        if name not in self.scalars:
            raise InvalidServiceConfiguration(
                'Invalid Service Argument Scalar "%s" (not found)' % name
            )
        new_value = self.scalars.get(name)
        return new_value

    def _replace_scalar(self, scalar):
        """ Replace scalar name with scalar value """
        if not is_arg_scalar(scalar):
            return scalar
        name = scalar[1:]
        return self.get_scalar_value(name)

    def _replace_service(self, service):
        """ Replace service name with service instance """
        if not is_arg_service(service):
            return service
        return self.get_instantiated_service(service[1:])

    def _instantiate(self, module, class_name,
                     args=None, kwargs=None, static=None):
        """ Instantiates a class if provided """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        if static is None:
            static = False

        _check_type('args', args, list)
        _check_type('kwargs', kwargs, dict)

        if static and class_name is None:
            return module

        if static and class_name is not None:
            return getattr(module, class_name)

        service_obj = getattr(module, class_name)

        # Replace scalars
        args = self._replace_scalars_in_args(args)
        kwargs = self._replace_scalars_in_kwargs(kwargs)

        # Replace service references
        args = self._replace_services_in_args(args)
        kwargs = self._replace_services_in_kwargs(kwargs)


        # Instantiate object
        return service_obj(*args, **kwargs)

    def _handle_factory_method(self, service_obj, method_name,
                               args=None, kwargs=None):
        """" Returns an object returned from a factory method """
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}

        _check_type('args', args, list)
        _check_type('kwargs', kwargs, dict)

        # Replace args
        new_args = self._replace_scalars_in_args(args)
        new_kwargs = self._replace_scalars_in_kwargs(kwargs)

        return getattr(service_obj, method_name)(*new_args, **new_kwargs)

    def _handle_calls(self, service_obj, calls):
        """ Performs method calls on service object """

        for call in calls:
            method = call.get('method')
            args = call.get('args', [])
            kwargs = call.get('kwargs', {})

            _check_type('args', args, list)
            _check_type('kwargs', kwargs, dict)

            if method is None:
                raise InvalidServiceConfiguration(
                    'Service call must define a method.'
                )

            new_args = self._replace_scalars_in_args(args)
            new_kwargs = self._replace_scalars_in_kwargs(kwargs)
            getattr(service_obj, method)(*new_args, **new_kwargs)
