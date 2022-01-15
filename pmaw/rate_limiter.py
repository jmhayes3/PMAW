import time

from pmaw import log as logger


class RateLimiter:

    def __init__(self):
        self.remaining = None
        self.limit = None
        self.reset_timestamp = None
        self.next_request_timestamp = None
        self.wait = 1

    def call(self, request_function, *args, **kwargs):
        self.delay()
        response = request_function(*args, **kwargs)
        self.update(response.headers)
        return response

    def delay(self):
        if self.next_request_timestamp is not None:
            _wait = self.next_request_timestamp - time.time()
            if _wait <= 0:
                return
            else:
                logger.debug(f"Sleeping {_wait} seconds prior to call")
                time.sleep(_wait)

    def update(self, response_headers):
        self.remaining = int(response_headers["x-ratelimit-remaining"])
        self.limit = int(response_headers["x-ratelimit-limit"])
        self.reset_timestamp = int(response_headers["x-ratelimit-reset"])

        logger.debug(f"Remaining: {self.remaining}")
        logger.debug(f"Limit: {self.limit}")
        logger.debug(f"Ratelimit reset: {self.reset_timestamp}")

        if self.remaining <= 0:
            self.next_request_timestamp = self.reset_timestamp
        else:
            self.next_request_timestamp = min(self.reset_timestamp, time.time() + self.wait)
