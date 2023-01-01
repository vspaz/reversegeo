import logging
import os
import sys


def configure_logger(logger_config):
    params = {
        "stream": sys.stderr,
        "level": logging.INFO,
        "format": "%(asctime)s.%(msecs)03d %(levelname)s: %(message)s",
        "datefmt": "%Y-%m-%d %X",
    }

    if logger_config:
        logdir = logger_config.get("logdir", ".")
        log_file_name = logger_config.get("log_file_name")
        if log_file_name:
            params["filename"] = os.path.join(logdir, log_file_name)
            del params["stream"]

    logging.basicConfig(**params)
    return logging.getLogger(__name__)
