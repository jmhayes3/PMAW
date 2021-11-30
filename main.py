import os
import logging
import time

from datetime import datetime, timezone

from pmaw import setup_logging, Authenticator, RequestHandler, Session, API_PATH, TooManyRequests, ResponseException


def main(debug=False):
    log_level = logging.INFO

    if debug:
        log_level = logging.DEBUG

    setup_logging(log_level=log_level)

    logger = logging.getLogger("pmaw")

    auth = Authenticator(
        os.environ["X_MESSARI_API_KEY"],
    )
    request_handler = RequestHandler(auth=auth)
    # request_handler = RequestHandler(auth=None)

    session = Session(request_handler)

    while True:
        try:
            response = session.request(
                "GET",
                API_PATH.get("assets"),
            )
        except TooManyRequests as e:
            logger.info(e)
        except ResponseException as e:
            logger.error(e)


if __name__ == "__main__":
    main(debug=True)
