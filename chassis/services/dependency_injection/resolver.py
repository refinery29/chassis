""" Resolver module """

import six

from chassis.services.dependency_injection import ServiceFactory
from chassis.util.tree import DependencyNode
from chassis.util.tree import DependencyTree


class CircularDependencyException(Exception):
    """ Raised when a circular dependency graph is detected """
    def __init__(self, nodes):
        super(CircularDependencyException, self).__init__()
        self.node_path = '->'.join(nodes)
        self.message = "Circular Depedency Detected: %s" % self.node_path


def detect_circle(nodes):
    """ Wrapper for recursive _detect_circle function """
    # Verify nodes and traveled types
    if not isinstance(nodes, dict):
        raise TypeError('"nodes" must be a dictionary')

    dependencies = set(nodes.keys())
    traveled = []

    heads = _detect_circle(nodes, dependencies, traveled)

    return DependencyTree(heads)


def _detect_circle(nodes=None, dependencies=None, traveled=None, path=None):
    """
        Recursively iterate over nodes checking
        if we've traveled to that node before.
    """
    # Verify nodes and traveled types
    if nodes is None:
        nodes = {}
    elif not isinstance(nodes, dict):
        raise TypeError('"nodes" must be a dictionary')
    if dependencies is None:
        return
    elif not isinstance(dependencies, set):
        raise TypeError('"dependencies" must be a set')
    if traveled is None:
        traveled = []
    elif not isinstance(traveled, list):
        raise TypeError('"traveled" must be a list')
    if path is None:
        path = []

    if not dependencies:
        # We're at the end of a dependency path.
        return []

    # Recursively iterate over nodes,
    # and gather dependency children nodes.
    children = []
    for name in dependencies:
        # Path is used for circular dependency exceptions
        # to display to the user the circular path.
        new_path = list(path)
        new_path.append(name)

        # Check if we've traveled to this node before.
        if name in traveled:
            raise CircularDependencyException(new_path)

        # Make recursive call
        node_children = _detect_circle(nodes=nodes,
                                       dependencies=nodes[name],
                                       traveled=traveled + list(name),
                                       path=new_path)

        # Create node for this dependency with children.
        node = DependencyNode(name)
        for child in node_children:
            child.parent = node
            node.add_child(child)
        children.append(node)

    return children


def solve(nodes):
    """ Solve graph into Solution """
    # Verify nodes type
    if not isinstance(nodes, dict):
        raise TypeError('"nodes" must be a dictionary')

    # Check for circular dependencies
    return detect_circle(nodes)


def is_dependency_name(name):
    """ Returns true if of the form "@some_string" """
    if not isinstance(name, str):
        return False
    return name[0:1] == '@'


class Resolver(object):
    """ Resolves dependency node graph and instantiates services """
    def __init__(self, config, scalars=None):
        """ Initialize Resolver """
        if scalars is None:
            scalars = {}
        self._nodes = {}
        self._config = config
        self._factory = ServiceFactory(scalars)
        self._init_nodes(config)

    @property
    def nodes(self):
        """ Return nodes """
        return self._nodes

    # pylint: disable=invalid-name
    def do(self):
        """ Instantiate Services """
        if not self._nodes:
            return
        # Let's retain original copy of _nodes
        node_copy = dict(self._nodes)

        self._do(node_copy)

        return self._factory.get_instantiated_services()

    def _do(self, nodes):
        """ Recursive method to instantiate services """
        if not isinstance(nodes, dict):
            raise TypeError('"nodes" must be a dictionary')

        if not nodes:
            # we're done!
            return
        starting_num_nodes = len(nodes)
        newly_instantiated = set()

        # Instantiate services with an empty dependency set
        for (name, dependency_set) in six.iteritems(nodes):
            if dependency_set:
                # Skip non-empty dependency sets
                continue

            # Instantiate
            config = self._config[name]
            service = self._factory.create_from_dict(config)
            self._factory.add_instantiated_service(name, service)

            newly_instantiated.add(name)

        # We ALWAYS should have instantiated a new service
        # or we'll end up in an infinite loop.
        if not newly_instantiated:
            raise Exception('No newly instantiated services')

        # Remove from Nodes
        for name in newly_instantiated:
            del nodes[name]

        # Check if the number of nodes have changed
        # to prevent infinite loops.
        # We should ALWAYS have removed a node.
        if starting_num_nodes == len(nodes):
            raise Exception('No nodes removed!')

        # Remove newly instantiated services from dependency sets
        for (name, dependency_set) in six.iteritems(nodes):
            nodes[name] = dependency_set.difference(newly_instantiated)

        # Recursion is recursion is ...
        self._do(nodes)

    def _init_nodes(self, config):
        """ Gathers dependency sets onto _nodes """
        if not isinstance(config, dict):
            raise TypeError('"config" must be a dictionary')

        for (name, conf) in six.iteritems(config):
            args = [] if 'args' not in conf else conf['args']
            kwargs = {} if 'kwargs' not in conf else conf['kwargs']

            dependencies = set()
            arg_deps = self._get_dependencies_from_args(args)
            kwarg_deps = self._get_dependencies_from_kwargs(kwargs)

            dependencies.update(arg_deps)
            dependencies.update(kwarg_deps)

            self._nodes[name] = dependencies

    def _get_dependencies_from_args(self, args):
        """ Parse arguments """
        if not isinstance(args, list):
            raise TypeError('"args" must be a list')

        dependency_names = set()
        for arg in args:
            new_names = self._check_arg(arg)
            dependency_names.update(new_names)
        return dependency_names

    def _get_dependencies_from_kwargs(self, args):
        """ Parse keyed arguments """
        if not isinstance(args, dict):
            raise TypeError('"kwargs" must be a dictionary')

        dependency_names = set()
        for arg in args.values():
            new_names = self._check_arg(arg)
            dependency_names.update(new_names)
        return dependency_names

    def _check_arg(self, arg):
        """ Check individual argument (list/tuple/string/etc) """
        if isinstance(arg, list):
            return self._get_dependencies_from_args(arg)
        elif isinstance(arg, dict):
            return self._get_dependencies_from_kwargs(arg)

        if not is_dependency_name(arg):
            return set()
        return set([arg[1:]])
