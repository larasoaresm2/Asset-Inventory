import logging
import os
import time
from logging.handlers import RotatingFileHandler


def setup_logging(folder="data", level="INFO"):
    """Send log records to folder/app.log, rotating at 1 MB and keeping 3 old files.

    The log goes to a file, not to the screen, so it does not mix with the menu.
    Times are in UTC, the usual choice on servers.
    """
    os.makedirs(folder, exist_ok=True)
    handler = RotatingFileHandler(
        os.path.join(folder, "app.log"), maxBytes=1_000_000, backupCount=3, encoding="utf-8"
    )
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%SZ"
    )
    formatter.converter = time.gmtime
    handler.setFormatter(formatter)
    logging.basicConfig(level=level, handlers=[handler], force=True)
