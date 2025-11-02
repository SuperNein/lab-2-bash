import logging
from pathlib import Path

def logging_config(level=logging.INFO):
    current_file = Path(__file__).resolve()
    filename = current_file.parent.parent.parent / 'shell.log'

    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(levelname)8s: %(message)s",
        filename=filename,
    )
