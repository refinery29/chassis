# pylint: disable=missing-docstring, no-self-use
# pylint: disable=too-few-public-methods, blacklisted-name


class Foo(object):
    @property
    def value(self):
        return 'foo'


class Bar(object):
    def __init__(self, foo):
        self._foo = foo

    @property
    def value(self):
        return self._foo.value + 'bar'


class Baz(object):
    @property
    def value(self):
        return 'baz'


class Qux(object):
    def __init__(self, foo, bar, baz):
        self._foo = foo
        self._bar = bar
        self._baz = baz

    @property
    def value(self):
        return self._foo.value + self._bar.value + self._baz.value + 'qux'


class Spam(object):
    def __init__(self, ham=None, eggs=None):
        self._ham = ham
        self._eggs = eggs

    @property
    def ham(self):
        return self._ham

    def set_ham(self, ham):
        self._ham = ham

    @property
    def eggs(self):
        return self._eggs

    def set_eggs(self, eggs=None):
        self._eggs = eggs


class Factory(object):
    @classmethod
    def get_foo(cls):
        return Foo()

    @classmethod
    def get_spam(cls, ham, eggs):
        return Spam(ham, eggs)

    @classmethod
    def get_more_spam(cls, ham='MAH', eggs='sgge'):
        return Spam(ham, eggs)


class Wibble(object):
    value = 'wobble'

    def __init__(self):
        self.value = 'webble'


class Wobble(object):
    def __init__(self, foo=None, bar=None, baz=None, spam=None):
        self._foo = foo
        self._bar = bar
        self._baz = baz
        self._spam = spam

    @property
    def foo(self):
        return self._foo

    @property
    def bar(self):
        return self._bar

    @property
    def baz(self):
        return self._baz

    @property
    def spam(self):
        return self._spam


class Weeble(object):
    def __init__(self, config):
        self._config = config

    def find(self, key):
        return self._config[key]


class TestLogger(object):
    def __init__(self, *arg, **kwargs):
        self._config = arg[0]

    @property
    def config(self):
        return self._config
