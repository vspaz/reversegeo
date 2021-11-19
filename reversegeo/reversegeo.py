import json
import os
import sys

from fileops import from_files, get_csv_dump_path, get_files, to_csv
from filters import get_european_country_and_city
from googleapiclient import GoogleApiClient
from reversegeo import cli
from reversegeo.__version__ import __version__
from reversegeo.log import configure_logger


def main():
    args = cli.get_args()
    config = json.loads(args.config)

    logger = configure_logger(logger_config=config.get('logging'))
    logger.info(f'reversegeo {__version__!r}')
    logger.info(f'PID = {os.getpid()}')

    gclient = GoogleApiClient(config=config)
    logger.info('Trying to read from the csv source file(s)')

    csv_files = get_files(dirs=args.source, pattern=args.files)
    coordinates = from_files(files=csv_files)
    logger.info('Processing started')
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
            logger.info('Processing interrupted')
            sys.exit(0)
        except Exception as e:
            logger.error('%s for coordinates %s', e, coord)
        total_count += 1
    logger.info('Processing complete')
    logger.info('Processed %s records', total_count)
    logger.info('Shut down')


if __name__ == '__main__':
    main()
