"""Utility Decorators for Chassis Applications."""


def include_original(dec):
    """Decorate decorators so they include a copy of the original function."""
    def meta_decorator(method):
        """Yo dawg, I heard you like decorators..."""
        # pylint: disable=protected-access
        decorator = dec(method)
        decorator._original = method
        return decorator
    return meta_decorator
