""" Unit Tests for Resolver Module """
import unittest
import yaml

from chassis.test.example_classes import Bar
from chassis.test.example_classes import Baz
from chassis.test.example_classes import Foo
from chassis.test.example_classes import Spam
from chassis.test.example_classes import Qux
from chassis.test.example_classes import Wobble
from chassis.test.example_classes import TestLogger
import chassis.services.dependency_injection.resolver as resolver
from chassis.util.tree import DependencyTree


def get_config_yaml():
    """ Load test config YAML file """
    return yaml.load(open(
        'test/services/dependency_injection/test_config.yml',
        'r')) or {}


class DetectCircleTest(unittest.TestCase):
    """ Unit Tests for detect_circle method """
    # pylint: disable=no-self-use, invalid-name
    def test_detect_circle_raises_circular_exception(self):
        """
            Check that Circular Dependencies are
            detected and an exception is raised.
        """
        self.assertRaises(resolver.CircularDependencyException,
                          resolver.detect_circle,
                          {'a': set(['b']),
                           'b': set(['a'])})

        self.assertRaises(resolver.CircularDependencyException,
                          resolver.detect_circle,
                          {'a': set(['b']),
                           'b': set(['c']),
                           'c': set(['a'])})

    # pylint: disable=invalid-name
    def test_detect_circle_raises_type_exception(self):
        """
            Check that invalid argument types are
            detected and an exception is raised.
        """
        self.assertRaises(TypeError,
                          resolver._detect_circle,
                          'not_a_dictionary')

        self.assertRaises(TypeError,
                          resolver._detect_circle,
                          {'a': ()},
                          'not_a_tuple')

        self.assertRaises(TypeError,
                          resolver._detect_circle,
                          {'a': ()},
                          (),
                          'not_a_list')

        self.assertRaises(TypeError,
                          resolver._detect_circle,
                          {'a': ()},
                          (),
                          [],
                          'not_an_integer')

        self.assertRaises(TypeError,
                          resolver._detect_circle,
                          {'a': ()},
                          (),
                          [],
                          0,
                          'not_a_list')

    # pylint: disable=no-self-use
    def test_detect_circle_2(self):
        """ Test another Circular Dependency Case """
        graph = {
            'a': set(['b']),
            'b': set(['c', 'd']),
            'c': set(['e']),
            'd': set(['e']),
            'e': set()
        }
        tree = resolver.detect_circle(graph)

        assert isinstance(tree, DependencyTree)

    def test_detect_circle(self):
        """
            Check that a Circular Dependency exception
            is not raised for a valid graph.
        """
        graph = {
            'a': set(['f', 'c']),
            'b': set(),
            'c': set(['b']),
            'd': set(),
            'e': set('d'),
            'f': set(),
            'g': set(['a'])
        }

        # Call Test Method
        tree = resolver.detect_circle(graph)
        assert isinstance(tree, DependencyTree)
        self.assertEquals(7, tree.head_count)
        self.assertEquals(
            set(['a', 'b', 'c', 'd', 'e', 'f', 'g']),
            tree.head_values
        )


class DependencyNameTest(unittest.TestCase):
    """ Is dependency method Unit Tests """
    # pylint: disable=no-self-use
    def test_names(self):
        """ Assert correct service string values are detected """
        assert resolver.is_dependency_name('@foo')
        assert not resolver.is_dependency_name('foo')


class ResolverTest(unittest.TestCase):
    """ Resolver class Unit Tests """
    def test_init_nodes(self):
        """ Simple init nodes test """
        config = {
            'foo': {
                'module': 'chassis.test.example_classes',
                'class': 'Foo'
            }
        }
        rslvr = resolver.Resolver(config)

        nodes = rslvr.nodes
        self.assertEquals(nodes['foo'], set())

    # pylint: disable=invalid-name
    def test_init_nodes_with_a_dependency(self):
        """ Init nodes with a dependency """
        config = {
            'foo': {
                'module': 'chassis.test.example_classes',
                'class': 'Foo'
            },
            'bar': {
                'module': 'chassis.test.example_classes',
                'class': 'Bar',
                'args': ['@foo']
            }
        }
        rslvr = resolver.Resolver(config)

        nodes = rslvr.nodes
        self.assertEquals(nodes['foo'], set())
        self.assertEquals(nodes['bar'], set(['foo']))

    def test_init_nodes_complicated(self):
        """ Initialize nodes with advanced config YAML file """
        config = get_config_yaml()
        rslvr = resolver.Resolver(config)

        nodes = rslvr.nodes
        self.assertEquals(nodes['baz'], set())
        self.assertEquals(nodes['foo'], set())
        self.assertEquals(nodes['bar'], set(['foo']))
        self.assertEquals(nodes['qux'], set(['foo', 'bar', 'baz']))

    def test_do_simple(self):
        """ Simple config resolution """
        rslvr = resolver.Resolver({
            'foo': {
                'module': 'chassis.test.example_classes',
                'class': 'Foo'
            }
        })

        services = rslvr.do()

        self.assertTrue('foo' in services)
        assert isinstance(services['foo'], Foo)

    def test_advanced(self):
        config = {
            'logger': {
                'module': 'chassis.test.example_classes',
                'class': 'TestLogger',
                'args': [
                    {
                        'name': 'test_logger',
                        'path': '/var/foo',
                        'file_base_name': 'testlog',
                        'max_file_bytes': 500,
                        'backup_count': 10,
                        'port': '$_port'
                    }
                ]
            }
        }
        scalars = {'_port': 555}
        rslvr = resolver.Resolver(config, scalars)

        services = rslvr.do()
        logger = services['logger']

        assert isinstance(logger, TestLogger)
        self.assertEquals(
            {
                'name': 'test_logger',
                'path': '/var/foo',
                'file_base_name': 'testlog',
                'max_file_bytes': 500,
                'backup_count': 10,
                'port': 555
            },
            logger.config
        )

    def test_do_complicated(self):
        """ Instantiate services from advanced YAML file """
        config = get_config_yaml()
        rslvr = resolver.Resolver(config)

        services = rslvr.do()

        assert isinstance(services['foo'], Foo)
        assert isinstance(services['bar'], Bar)
        assert isinstance(services['baz'], Baz)
        assert isinstance(services['qux'], Qux)
        assert isinstance(services['wobble'], Wobble)
        assert isinstance(services['spam'], Spam)

        spam = services['spam']
        self.assertEquals(spam.ham, 'ham!')
        self.assertEquals(spam.eggs, 'eggz')

        wobble = services['wobble']
        assert isinstance(wobble.foo, Foo)
        assert isinstance(wobble.bar, Bar)
        assert isinstance(wobble.baz, Baz)
        assert isinstance(wobble.spam, Spam)
