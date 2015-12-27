



import time
import functools

def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return _wrapper
