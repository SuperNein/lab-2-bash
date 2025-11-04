import logging
from shlex import split as shlex_split

from src.common.config import logging_config
from src.services.console import Console

logger = logging.getLogger(__name__)
logging_config(level=logging.DEBUG)


def cmdline_to_kwargs(cmd_line: str) -> dict[str, str | list[str]]:
    """
    Convert stdin from cmd line to dictionary with keys:
    cmd, options, args

    :param cmd_line:    stdin from cmd
    :return:    dictionary type: {cmd: str, options: list[str], args: list[str]}
    """
    try:
        args = shlex_split(cmd_line)
    except ValueError as e:
        logger.error(f'Invalid arguments: {e}')
        raise SyntaxError(e)

    kwargs = {
        'cmd': '',
        'options': [],
        'args': []
    }

    try:
        kwargs['cmd'] = args.pop(0)
    except IndexError:
        return kwargs

    for element in args[:]:
        if element[0] == '-':
            kwargs['options'].append(element)
            args.remove(element)

    kwargs['args'] = args
    return kwargs


def console_handling(console: Console, cmd_line: str):
    kwargs = cmdline_to_kwargs(cmd_line)
    stdout: list = []

    logger.debug(kwargs)

    match kwargs['cmd']:
        case 'exit' | 'quit' | 'q':
            console.exit(**kwargs)
        case 'ls':
            stdout = console.ls(**kwargs)
        case 'cd':
            console.cd(**kwargs)
        case 'cat':
            stdout = console.cat(**kwargs)
        case '':
            pass
        case _:
            logger.error(f'Unknown command: {kwargs['cmd']}')
            raise RuntimeError(f'{kwargs['cmd']}: command not found')

    return stdout
