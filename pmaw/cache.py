class cachedproperty:
    """A decorator for caching a property's result.

    Similar to `property`, but the wrapped method's result is cached on the instance.
    This is achieved by setting an entry in the object's instance dictionary with the
    same name as the property. When the name is later accessed, the value in the
    instance dictionary takes precedence over the (non-data descriptor) property.

    This is useful for implementing lazy-loaded properties.

    The cache can be invalidated via `delattr()`, or by modifying `__dict__` directly.
    It will be repopulated on next access.
    """

    def __init__(self, func, doc=None):
        """Initialize the descriptor."""
        self.func = self.__wrapped__ = func

        if doc is None:
            doc = func.__doc__
        self.__doc__ = doc

    # This to make sphinx run properly
    def __call__(self, *args, **kwargs):  # pragma: no cover noqa: D102
        pass

    def __get__(self, obj=None, objtype=None):
        """Implement descriptor getter.

        Calculate the property's value and then store it in the associated object's
        instance dictionary.

        """
        if obj is None:
            return self

        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value

    def __repr__(self):
        """Return repr(self)."""
        return f"<{self.__class__.__name__} {self.func}>"


_missing = object()

class cached_property(object):
    """A decorator that converts a function into a lazy property.  The
    function wrapped is called the first time to retrieve the result
    and then that calculated result is used the next time you access
    the value::

    class Foo(object):

        @cached_property
        def foo(self):
            # calculate something important here
            return 42

    The class has to have a `__dict__` in order for this property to
    work.
    """

    # implementation detail: this property is implemented as non-data
    # descriptor.  non-data descriptors are only invoked if there is
    # no entry with the same name in the instance's __dict__.
    # this allows us to completely get rid of the access function call
    # overhead.  If one choses to invoke __get__ by hand the property
    # will still work as expected because the lookup logic is replicated
    # in __get__ for manual invocation.

    def __init__(self, func, name=None, doc=None):
        self.__name__ = name or func.__name__
        self.__module__ = func.__module__
        self.__doc__ = doc or func.__doc__
        self.func = func

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        value = obj.__dict__.get(self.__name__, _missing)
        if value is _missing:
            value = self.func(obj)
            obj.__dict__[self.__name__] = value
        return value
