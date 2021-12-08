import sys
import logging
import time
import random

from collections import OrderedDict
from collections.abc import MutableMapping


def flatten(data, parent="", sep="_"):
    items = []
    for k, v in data.items():
        new_key = parent + sep + k if parent else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


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


def setup_logging(log_level=logging.INFO):
    log_format = logging.Formatter(
        (
            "%(asctime)s [%(levelname)s]"
            " -- [%(name)s:%(module)s/%(funcName)s]"
            " -- %(message)s"
        ),
        datefmt="%H:%M:%S"
    )

    null_handler = logging.NullHandler()
    logging.basicConfig(
        level=log_level,
        handlers=[null_handler]
    )

    # Set handler for logging to console.
    # console_handler = logging.StreamHandler()  # Log to stderr.
    console_handler = logging.StreamHandler(sys.__stdout__)  # Log to stdout.
    console_handler.setLevel(log_level)
    console_handler.setFormatter(log_format)

    logger = logging.getLogger()
    logger.addHandler(console_handler)


def stream_generator(function, pause_after=None, skip_existing=False, exclude_before=False, **function_kwargs):
    before_attribute = None
    exponential_counter = ExponentialCounter(max_counter=16)
    seen_attributes = BoundedSet(301)
    without_before_counter = 0
    responses_without_new = 0
    valid_pause_after = pause_after is not None

    while True:
        found = False
        newest_attribute = None
        limit = 100
        if before_attribute is None:
            limit -= without_before_counter
            without_before_counter = (without_before_counter + 1) % 30
        if not exclude_before:
            function_kwargs["params"] = {"before": before_attribute}
        for item in reversed(list(function(limit=limit, **function_kwargs))):
            attribute = getattr(item, "slug")
            if attribute in seen_attributes:
                continue
            found = True
            seen_attributes.add(attribute)
            newest_attribute = attribute
            if not skip_existing:
                yield item
        before_attribute = newest_attribute
        skip_existing = False
        if valid_pause_after and pause_after < 0:
            yield None
        elif found:
            exponential_counter.reset()
            responses_without_new = 0
        else:
            responses_without_new += 1
            if valid_pause_after and responses_without_new > pause_after:
                exponential_counter.reset()
                responses_without_new = 0
                yield None
            else:
                time.sleep(exponential_counter.counter())
