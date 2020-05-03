import time


def timing_decorator(func):
    """
    Annotation to counting elapsed time for method
    Prints it to console
    """
    def wrapper(*args, **kwargs):
        start = time.time()
        original_return_val = func(*args, **kwargs)
        end = time.time()

        print("time elapsed in ", func.__name__, ": ", end - start, sep='')

        return original_return_val

    return wrapper
