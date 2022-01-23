import time
import random

from collections import OrderedDict


class BoundedSet:
    """A set with a maximum size that evicts the oldest items when necessary.
    This class does not implement the complete set interface.
    """

    def __init__(self, max_items):
        """Construct an instance of the BoundedSet."""
        self.max_items = max_items
        self._set = OrderedDict()

    def __contains__(self, item):
        """Test if the BoundedSet contains item."""
        self._access(item)
        return item in self._set

    def _access(self, item):
        if item in self._set:
            self._set.move_to_end(item)

    def add(self, item):
        """Add an item to the set discarding the oldest item if necessary."""
        self._access(item)
        self._set[item] = None
        if len(self._set) > self.max_items:
            self._set.popitem(last=False)


# for use when no new data is returned
class ExponentialCounter:
    """A class to provide an exponential counter with jitter."""

    def __init__(self, max_counter):
        """The computed value may be 3.125% higher due to jitter."""

        self._base = 1
        self._max = max_counter

    def counter(self):
        """Increment the counter and return the current value with jitter."""
        max_jitter = self._base / 16.0
        value = self._base + random.random() * max_jitter - max_jitter / 2
        self._base = min(self._base * 2, self._max)
        return value

    def reset(self):
        """Reset the counter to 1."""
        self._base = 1
