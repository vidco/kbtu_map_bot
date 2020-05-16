import logging
import time

LOG = logging.getLogger('timer')


def timing_decorator(func):
    """
    Annotation to counting elapsed time for method
    Prints it to console
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        original_return_val = func(*args, **kwargs)
        end = time.time()

        LOG.info('time taken for %s is %d ms', func.__name__, (end - start) * 1000)

        return original_return_val

    return wrapper
