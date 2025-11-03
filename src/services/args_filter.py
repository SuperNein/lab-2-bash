import logging

from src.common.config import logging_config

logger = logging.getLogger(__name__)
logging_config(level=logging.DEBUG)


def options_filter(available_options: list[str] | None = None):
    if not available_options:
        available_options = ['']

    def decorator(func):
        def wrapper(*args, **kwargs):

            for option in kwargs['options']:
                if not (option in available_options):
                    logger.error(f'Invalid option for {kwargs['cmd']}: {option}')
                    raise ValueError(f'{kwargs['cmd']}: {option}: invalid option')

            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
