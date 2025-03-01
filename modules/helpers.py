import functools
import logging
import time

from modules.exceptions.exception import GGBotRetryException


def retry_on_failure(retries=3, delay=5):
    """
    Decorator factory that returns a decorator to retry a function upon encountering a GGBotRetryException.

    Args:
        retries (int): The maximum number of retry attempts. Default is 3.
        delay (int): The delay in seconds between retries. Default is 5 seconds.

    Returns:
        function: A decorator that applies the retry logic to the target function.
    """

    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            attempt = 1
            latest_exception = None
            while attempt <= retries:
                try:
                    return function(*args, **kwargs)
                except GGBotRetryException as e:
                    latest_exception = e
                    logging.error(
                        f"[RetryHelper] Attempt {attempt} failed for function '{function.__name__}': {e}. Retrying..."
                    )
                    attempt += 1
                    time.sleep(delay)
            logging.error(
                f"[RetryHelper] All {retries} attempts failed for function '{function.__name__}'."
            )
            raise latest_exception

        return wrapper

    return decorator
