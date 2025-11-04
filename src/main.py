import logging

from src.common.config import logging_config
from src.services.handler import console_handling
from src.services.console import Console
from src.states import current_dir as cwd


def main() -> None:
    """
    Main entry point for the application.
    :return: None
    """
    logger = logging.getLogger(__name__)
    logging_config(level=logging.DEBUG)

    while True:
        stdin = input(f'{cwd.current_dir}> ')
        logger.info(f'User input: {stdin!r}')

        console = Console(logger)

        try:
            stdout = console_handling(console, stdin)
            print(*stdout, sep='\n')
        except KeyboardInterrupt:
            exit()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
