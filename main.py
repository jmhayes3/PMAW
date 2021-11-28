import os
import logging
import time

from datetime import datetime, timezone

from pmaw import setup_logging, Authenticator, RequestHandler, Session, API_PATH


def main(debug=False):
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    setup_logging(log_level=log_level)

    auth = Authenticator(
        os.environ["X_MESSARI_API_KEY"],
    )
    # request_handler = RequestHandler(auth=auth)
    request_handler = RequestHandler(auth=None)

    session = Session(request_handler)

    for _ in range(20):
        response = session.request(
            "GET",
            API_PATH.get("assets"),
        )

        head = response.headers
        print(head)

        body = response.json()

        status = body.keys()
        print(body['status'])

        data = body["data"]

        print("Length: {}".format(len(data)))

        timestamp = int(head["x-ratelimit-reset"])
        dt = datetime.fromtimestamp(timestamp, timezone.utc)
        print(dt)

        print(response.request.headers)


if __name__ == "__main__":
    main(debug=True)
