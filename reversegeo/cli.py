#!/usr/bin/env python3

import argparse
import os

from reversegeo.__version__ import __version__
from reversegeo.config import ConfigValidator


def get_args():
    description = "utility to retrieve reverse geocoding data from Google API."
    app = "reversegeo"
    usage = f'{app} -c cfg.json -s [source] -d [dump] -f [files]'
    argparser = argparse.ArgumentParser(
        description=description,
        prog=app,
        usage=usage,
    )
    argparser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"'{__version__}'",
    )
    argparser.add_argument(
        "-c",
        "--config",
        type=argparse.FileType("r"),
        dest="config",
        required=True,
        action=ConfigValidator,
        help="absolute path to config.json",
    )
    argparser.add_argument(
        "-s",
        "--source",
        default=[os.path.join(os.getcwd(), "data")],
        type=str,
        nargs="+",
        help="absolute path to source directories",
    )
    argparser.add_argument(
        "-d",
        "--dump",
        default=os.path.join(os.getcwd(), "dump"),
        type=str,
        help="absolute path to dump directory",
    )
    argparser.add_argument(
        "-f",
        "--files",
        default="*.csv",
        type=str,
        help="filter csv files with a regular expression",
    )

    return argparser.parse_args()
