#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys

from __version__ import version
from config import ConfigValidator
from fileops import from_files, get_csv_dump_path, get_files, to_csv
from filters import get_european_country_and_city
from googleapiclient import GoogleApiClient


def get_args():
    description = 'utility to retrieve reverse geocoding data from google API.'
    prog = 'reversegeo'
    usage = '%(prog)s -c cfg.json -s [source] -d [dump] -f [files]'
    argparser = argparse.ArgumentParser(
        description=description,
        prog=prog,
        usage=usage,
    )
    argparser.add_argument(
        '-v',
        '--version',
        action='version',
        version="'{}'".format(version),
    )
    argparser.add_argument(
        '-c',
        '--config',
        type=argparse.FileType('r'),
        dest='config',
        required=True,
        action=ConfigValidator,
        help='absolute path to config.json',
    )
    argparser.add_argument(
        '-s',
        '--source',
        default=[os.path.join(os.getcwd(), 'data')],
        type=str,
        nargs='+',
        help='absolute path to source directories',
    )
    argparser.add_argument(
        '-d',
        '--dump',
        default=os.path.join(os.getcwd(), 'dump'),
        type=str,
        help='absolute path to dump directory',
    )
    argparser.add_argument(
        '-f',
        '--files',
        default='*.csv',
        type=str,
        help='filter csv files with a regular expression')

    args = argparser.parse_args()

    return args


def configure_logger(logger_config):
    params = {
        'stream': sys.stderr,
        'level': logging.INFO,
        'format': '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        'datefmt': '%Y-%m-%d %X'
    }

    if logger_config:
        logdir = logger_config.get('logdir', '.')
        log_file_name = logger_config.get('log_file_name')
        if log_file_name:
            params['filename'] = os.path.join(logdir, log_file_name)
            del params['stream']

    logging.basicConfig(**params)


def main():
    args = get_args()
    config = json.loads(args.config)

    configure_logger(logger_config=config.get('logging'))
    logging.info('reversegeo %s', version)
    logging.info('PID = %d', os.getpid())

    gclient = GoogleApiClient(config=config)
    logging.info('Trying to read from the csv source file(s)')

    csv_files = get_files(dirs=args.source, pattern=args.files)
    coordinates = from_files(files=csv_files)
    logging.info('Processing started')
    total_count = 0
    for coord in coordinates:
        try:
            response = gclient.fetch_geo_data(latlng=coord)
            country, city = get_european_country_and_city(resp=response)
            if not all([country, city]):
                continue
            fields = coord.split(',')
            fields.append(city.lower())
            dump_file_path = get_csv_dump_path(country=country,
                                               dump_directory=args.dump)
            to_csv(file_path=dump_file_path, fields=fields)
        except KeyboardInterrupt:
            logging.info('Processing interrupted')
            sys.exit(0)
        except Exception as e:
            logging.error('%s for coordinates %s', e, coord)
        total_count += 1
    logging.info('Processing complete')
    logging.info('Processed %s records', total_count)
    logging.info('Shut down')


if __name__ == '__main__':
    main()
