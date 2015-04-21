### Contents

- [Overview](#overview)
- [Scalars](#scalars)
- [Dependency Injection](#dependency-injection)
- [Resolver](#resolver)
- [ServiceFactory](#service-factory)
- [Yaml + Resolver](#yaml-resolver)


## <a name="overview"></a>Overview

### Dependency Resolution, Creation, and Injection

Chassis contains a dependency resolver and injection service. You must provide a dictionary containing valid service definitions and have the libraries/packages installed within your environment.

The main entry point for the dependency injection tool is to instantiate a `chassis.services.dependency_injection.resolver.Resolver` class with a valid service definition dictionary and provide an optional dictionary of scalar values.

A valid service dictionary has the form:

```python
service_definitions = {
	'service_name': {
		'module': ..., 				# string
		'class': ..., 				# string
		'args': [...], 				# list
		'kwargs': {...}, 			# dictionary
		'factory-method': ...,		# string
		'factory-args': [...],		# list
		'factory-kwargs': {...},	# dictionary
		'static': ..., 				# boolean
		'calls': [					# list
			{
				'method': ..., 		# string
				'args': [...], 		# list
				'kwargs': {...},		# dict
			},
			...
		]
	}
}
```


## <a name="scalars"></a>Scalars

Scalars are used in service definitions by prepending a `$` before the scalar name.

Scalars are essentially variables that are replaced within your service definitions. A dictionary must be provided to the Resolver containing keys that will act as variable names and their values.

### Example

```python
import chassis.services.dependency_injection.resolver as di_resolver

scalars = {
	'port' : 5555,
	'users_api_endpoint': '/api/users'
}

service_definitions = {
	'user_api': {
		'module': 'api_helpers',
		'class': 'UserApi',
		'kwargs': {
			'port': '$port',
			'endpoint': '$users_api_endpoint'
		}
	}
}

services = di_resolver.Resolver(service_definitions, scalars).do()
user_api = services['user_api'] 
```

The `user_api` service was instantiated via the following analagous import command:

```
from api_helpers import UserApi
user_api = UserApi(port=555, endpoint='/api/users')
```

## <a name="dependency-injection"></a>Dependency Injection

Dependencies are used in service definitions by prepending a `@` before the service name.


### Example

```python
	import chassis.services.dependency_injection.resolver as di_resolver
	
	service_definitions = {
		'foo': {
			'module': 'example',
			'class': 'Foo'
		},
		'bar': {
			'module': 'example',
			'class': 'Bar',
			'args': ['@foo']
		},
		'baz': {
			'module': 'example',
			'class': 'Baz',
			'args': ['@bar']
		}
	}
	
	services = di_resolver.Resolver(service_definitions).do()
	foo = services['foo'] # Instantiation of example.Foo
	bar = services['bar'] # Instantiation of example.Bar
	baz = services['baz'] # Instantiation of example.Baz
```

In the above example, the service definitions and their arguments were parsed. The Resolver will recognize the service arguments (declared via `@`), and instantiate the services in the proper order so no service arguments are missing.

The order of instantiation:

1. Foo
2. Bar with Foo
3. Baz with Bar.

### Example Usage with scalars and a single dependency

```python
import chassis.services.dependency_injection.resolver as di_resolver

scalars = {
	'port': '8080',
	'address': '127.0.0.1'
}

service_definitions = {
	'your_service_name': {
		'module': 'module.path',
		'class': 'TheClassName',
		'args': ['foo', 'bar'],
		'kwargs': {
			'keyword': 'argument',
			'port': '$port',
			'address': '$address'
		}
	},
	'another_service': {
		'module': 'another.module.path',
		'class': 'SomeClass',
		'args': ['@your_service_name']
	}
}

resolver = di_resolver.Resolver(service_definitions, scalars)
services = resolver.do()

your_service = services['your_service_name'] # Instantiation of 'module.path.TheClassName'
another_service = services['another_service'] # Instantiation of 'another.module.path.SomeClass'
```

The above example equates to instantiating the service via:

```python
from module.path import TheClassName

your_service = TheClassName('foo', 'bar', keyword='argument', port=8080, address='127.0.0.1')
another_service = SomeClass(your_service)
```


## <a name="resolver"></a>Resolver

As the above example shows, the Resolver is instantiated with a dictionary containing service definitions, then the method `do()`. The `do()` method instantiates the services and returns a "container" dictionary of the services by their name.


## <a name="service-factory"></a>ServiceFactory


You can use the service factory to manually instantiate services dynamically. The Resolver object uses this class to instantiate the services provided by the service configuration dictionary.

The `create(...)` method is meant to be used to create a service dynamically.

### Example Usage

```python
from chassis.services.dependency_injection import ServiceFactory

factory = ServiceFactory()

service = factory.create(
	'module.path',
	'TheClassName',
	['first_argument', 'second_argument']
) # Equates to module.path.TheClassName('first_argument', 'second_argument')
```

## <a name="yaml-resolver"></a>YAML + Resolver

An effective method of utilizing the Resolver is to define your service definitions within a filetype of your choice (XML, YAML, etc). Load the file and pass it into the Resolver.

### Example

```python
import yaml # pyyaml library
from chassis.services.dependency_injection.resolver as di_resolver

service_definitions = yaml.load(open('./services.yml', 'r'))
services = di_resolver.Resolver(service_definitions).do()
# Done
```