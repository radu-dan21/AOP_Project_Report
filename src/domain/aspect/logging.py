import logging
import os

from datetime import datetime

import aspectlib

from src.constants import LOGGING_ROOT


def get_logger() -> logging.Logger:
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        os.path.join(
            LOGGING_ROOT,
            "debug_" + str(datetime.now()).replace(":", "-") + ".log",
        ),
        "w",
    )
    logger_.addHandler(handler)
    return logger_


logger = get_logger()


@aspectlib.Aspect(bind=True)
def logging_aspect(cutpoint, *args, **kwargs):
    logger.debug(
        f"Calling method: {cutpoint.__name__}; " f"args: {args}; " f"kwargs: {kwargs}"
    )
    result = yield aspectlib.Proceed
    yield aspectlib.Return(result)
