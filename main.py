import os
import sys
import logging
import traceback

from pmaw.auth import Authenticator
from pmaw.request_handler import RequestHandler
from pmaw.session import Session
from pmaw.exceptions import TooManyRequests, ResponseException
from pmaw.util import setup_logging
from pmaw.messari import Messari


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
    session = Session(request_handler)
    messari = Messari(session=session)

    try:
        asset = messari.asset(id="ethereum")
        print(asset)
        print(vars(asset))
        print(asset.symbol)
        print(asset)
        for i in asset.contract_addresses:
            print(i)
        for i in vars(asset):
            print(i)
        # metrics = asset.metrics
        # s = metrics.market_data
        # print(s)
        # for i in vars(metrics):
        #     print(i)
        p = asset.profile
        # print(p)
        g = p.general
        for i in vars(p):
            print(i)

        print(g.keys())
    except TooManyRequests as e:
        logger.warning(e)
    except ResponseException as e:
        logger.error(e)
    except:
        logger.critical("Uncaught exception: {}".format(
                traceback.format_exc()
            )
        )
        sys.exit(-1)


if __name__ == "__main__":
    main(debug=True)
