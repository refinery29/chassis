""" Tree Module """


class DependencyNode(object):
    """ Dependency Node class """
    def __init__(self, value):
        """ Initialize Node """
        self._parent = None
        self._children = []
        self._value = value

    @property
    def parent(self):
        """ Return parent node """
        return self._parent

    @parent.setter
    def parent(self, parent):
        """ Set parent node """
        self._parent = parent

    @property
    def value(self):
        """ Return value """
        return self._value

    @property
    def children(self):
        """ Get Children """
        return self._children

    @property
    def child_count(self):
        """ Get child count """
        return len(self._children)

    def add_child(self, child):
        """ Add a child node """
        if not isinstance(child, DependencyNode):
            raise TypeError('"child" must be a DependencyNode')
        self._children.append(child)

    def add_children(self, children):
        """ Add multiple children """
        if not isinstance(children, list):
            raise TypeError('"children" must be a list')
        for child in children:
            self.add_child(child)

    def __str__(self):
        if not self._children:
            return "(%s)" % self._value

        children_strings = []
        for child in self._children:
            children_strings.append(str(child))
        return "(%s, [%s])" % (self._value, ", ".join(children_strings))


class DependencyTree(object):
    """ Dependency Tree class """
    def __init__(self, heads):
        """ Initialize Tree """
        self._heads = []
        if heads is not None:
            if not isinstance(heads, list):
                raise TypeError('"head" must be a list')
            for head in heads:
                self.add_head(head)

    @property
    def heads(self):
        """ Get heads """
        return self._heads

    @property
    def head_values(self):
        """ Return set of the head values """
        values = set()
        for head in self._heads:
            values.add(head.value)
        return values

    @property
    def head_count(self):
        """ Get head count """
        return len(self._heads)

    def __str__(self):
        head_strings = []
        for head in self._heads:
            head_strings.append("H" + str(head))
        return ", ".join(head_strings)

    def add_head(self, head):
        """ Add head Node """
        if not isinstance(head, DependencyNode):
            raise TypeError('"head" must be a DependencyNode')
        self._heads.append(head)
