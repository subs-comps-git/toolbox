"""Decorator that logs execution times of the decorated function."""


import time
import functools


def logged(time_format, name_prefix=''):
    def decorator(func):
        if hasattr(func, '_logged_decorator') and func._logged_decorator:
            return func

        @functools.wraps(func)
        def decorated_func(*args, **kwargs):
            start_time = time.time()
            print('- Running {name} on {time}'.format(
                  name=name_prefix + func.__name__,
                  time=time.strftime(time_format))
                  )
            result = func(*args, **kwargs)
            end_time = time.time()
            print('- Finished {name}, execution time = {time}'.format(
                  name=name_prefix + func.__name__,
                  time=end_time - start_time)
                  )
            return result
        decorated_func._logged_decorator = True
        return decorated_func
    return decorator


def log_method_calls(time_format):
    def decorator(cls):
        for o in dir(cls):
            if o.startswith('__'):
                continue
            attribute = getattr(cls, o)
            if hasattr(attribute, '__call__'):
                decorated_attribute = logged(time_format,
                                             cls.__name__ + ".")(attribute)
                setattr(cls, o, decorated_attribute)
        return cls
    return decorator
