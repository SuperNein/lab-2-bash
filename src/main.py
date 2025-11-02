import logging

from src.common.config import logging_config
from src.services.splitter import split_by_args


def main() -> None:
    logger = logging.getLogger(__name__)
    logging_config(level=logging.DEBUG)

    while True:
        user_input = input('> ')
        cmd_args = split_by_args(user_input)
        cmd = cmd_args.pop(0)

        match cmd:
            case 'exit' | 'quit' | 'q':
                logger.info(user_input)
                logger.debug('Exit the program')
                break
            case _:
                logger.warning('Unknown command')
                print(f'Command {cmd!r} not found')


if __name__ == '__main__':
    main()
