import os
from pathlib import Path

TRASH_DIR = Path(__file__).parent.parent.parent / ".trash"
TRASH_DIR.mkdir(exist_ok=True)

HISTORY_DIR = Path(__file__).parent.parent.parent / ".history"