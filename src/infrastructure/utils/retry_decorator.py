import asyncio
import logging
from functools import wraps

def async_retry(max_retries: int = 3, delay: int = 2, backoff: int = 2):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 0
            current_delay = delay
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        logging.error(f"Function {func.__name__} failed after {max_retries} retries. Error: {e}")
                        raise
                    
                    logging.warning(f"Attempt {retries}/{max_retries} for {func.__name__} failed. Retrying in {current_delay}s. Error: {e}")
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
        return wrapper
    return decorator
