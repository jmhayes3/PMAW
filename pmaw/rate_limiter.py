import time


class RateLimiter:

    def __init__(self, target_rate=20):
        self.target_rate = target_rate

        self.remaining = None
        self.limit = None
        self.reset_timestamp = None
        self.next_request_timestamp = None
        self.cache = list()

    def call(self, request_function, *args, **kwargs):
        self.delay()
        response = request_function(*args, **kwargs)
        self.update(response.headers)
        return response

    def delay(self):
        if self.next_request_timestamp is not None:
            wait = self.next_request_timestamp - time.time()
            if wait <= 0:
                return
            else:
                time.sleep(wait)

    def update(self, response_headers):
        try:
            self.remaining = int(response_headers["x-ratelimit-remaining"])
            self.limit = int(response_headers["x-ratelimit-limit"])
            self.reset_timestamp = int(response_headers["x-ratelimit-reset"])
        except KeyError:
            return

        now = time.time()

        self.cache.append(now)

        start = min(self.cache)
        while now - start >= 60:
            try:
                self.cache.remove(start)
            except ValueError:
                pass
            start = min(self.cache)

        if self.remaining <= 0:
            self.next_request_timestamp = self.reset_timestamp
        else:
            delay = now + self.average()
            self.next_request_timestamp = min(
                self.reset_timestamp,
                delay
            )

    def average(self):
        requests = len(self.cache)
        start = min(self.cache)
        end = max(self.cache)

        interval = end - start
        if interval <= 0:
            return 0

        projected_rate = 60 * requests / interval
        if projected_rate < self.target_rate:
            return 0

        delay = (60 * requests / self.target_rate) - interval

        return delay
