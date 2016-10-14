import os
import binascii
import functools
import time


def timer(original_function, number=1000):
    @functools.wraps(original_function)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        for i in range(number):
            result = original_function(*args, **kwargs)
        end_time = time.time()
        print('function: {} args: {} took: {} secs'.format(
              original_function.__name__, args, (end_time - start_time) / number))
        return result
    return wrapped


def random_hex(length):
    return binascii.hexlify(os.urandom(length)).decode()
