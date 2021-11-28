import time
import logging

logger = logging.getLogger(__name__)


# for use when no new data is returned
class ExponentialCounter:
    """A class to provide an exponential counter with jitter."""

    def __init__(self, max_counter):
        # The computed value may be 3.125% higher due to jitter.

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


class RateLimiter:

    def __init__(self):
        self.remaining = None
        self.next_request_timestamp = None
        self.reset_timestamp = None
        self.limit_per_min = None
        self.limit_per_day = None
        self.rate = None

    def call(self, request_function, *args, **kwargs):
        self.delay()
        response = request_function(*args, **kwargs)
        self.update(response.headers)
        return response

    def delay(self):
        if self.next_request_timestamp is None:
            return

        _wait = self.next_request_timestamp - time.time()
        if _wait <= 0:
            return

        logger.info(f"Sleeping {_wait} seconds prior to call")
        time.sleep(_wait)

    def update(self, response_headers):
        if "x-ratelimit-remaining" not in response_headers:
            if self.remaining is not None:
                self.remaining -= 1
            return

        now = time.time()

        seconds_to_reset = int(response_headers["x-ratelimit-reset"])
        self.remaining = int(response_headers["x-ratelimit-remaining"])
        self.reset_timestamp = seconds_to_reset
        self.limit = int(response_headers["x-ratelimit-limit"])

        logger.info(f"Remaining: {self.remaining}")
        logger.info(f"Reset timestamp: {self.reset_timestamp}")
        logger.info(f"Limit: {self.limit}")

        if self.remaining <= 0:
            self.next_request_timestamp = self.reset_timestamp
            return

        self.next_request_timestamp = min(
            self.reset_timestamp,
            now + max(min(seconds_to_reset - self.remaining, 1), 0)
        )
