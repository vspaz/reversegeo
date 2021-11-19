import json
import logging
import os
import sys

from fileops import from_files, get_csv_dump_path, get_files, to_csv
from filters import get_european_country_and_city
from googleapiclient import GoogleApiClient
from reversegeo import cli
from reversegeo.__version__ import __version__


def configure_logger(logger_config):
    params = {
        'stream': sys.stderr,
        'level': logging.INFO,
        'format': '%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
        'datefmt': '%Y-%m-%d %X',
    }

    if logger_config:
        logdir = logger_config.get('logdir', '.')
        log_file_name = logger_config.get('log_file_name')
        if log_file_name:
            params['filename'] = os.path.join(logdir, log_file_name)
            del params['stream']

    logging.basicConfig(**params)


def main():
    args = cli.get_args()
    config = json.loads(args.config)

    configure_logger(logger_config=config.get('logging'))
    logging.info(f'reversegeo {__version__}!r')
    logging.info(f'PID = {os.getpid()}')

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
            dump_file_path = get_csv_dump_path(
                country=country,
                dump_directory=args.dump,
            )
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
