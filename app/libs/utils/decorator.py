import datetime
import logging
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


def timer(fn: Callable):
    """Timer decorator to record running time"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        start = datetime.datetime.utcnow()
        result = fn(*args, **kwargs)
        end = datetime.datetime.utcnow()
        logger.info('[timer] function={} timeTakenMillis={:.1f}ms'.format(fn.__name__, (end - start).seconds * 1000))
        return result
    return wrapper
