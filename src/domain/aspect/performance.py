import logging
import os

from datetime import datetime
from time import perf_counter

import aspectlib

from src.constants import LOGGING_ROOT


def get_logger() -> logging.Logger:
    logger_ = logging.getLogger(__name__)
    logger_.setLevel(logging.INFO)
    handler = logging.FileHandler(
        os.path.join(
            LOGGING_ROOT,
            "perf_info_" + str(datetime.now()).replace(":", "-") + ".log",
        ),
        "w",
    )
    logger_.addHandler(handler)
    return logger_


logger = get_logger()


@aspectlib.Aspect(bind=True)
def performance_aspect(cutpoint, *args, **kwargs):
    start_time: float = perf_counter()
    result = yield aspectlib.Proceed
    end_time: float = perf_counter()

    logger.info(f"Method <{cutpoint.__name__}> took {end_time - start_time} seconds")
    yield aspectlib.Return(result)
