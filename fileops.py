import glob
import csv
import os


def _from_csv(file):
    with open(file) as fh:
        line = fh.readline()  # skip header
        while line:
            # no need to parse csv until rows are filtered.
            line = fh.readline().strip()
            if line:
                yield line


def from_files(files):
    for file in files:
        for rec in _from_csv(file):
            yield rec


def to_csv(file_path, fields):
    if not os.path.exists(file_path):
        open(file_path, "x").close()
    with open(file_path, "a") as fh:
        writer = csv.writer(fh)
        writer.writerow(fields)


def get_files(dirs, pattern):
    csv_files = []
    for dir_ in dirs:
        files = glob.glob(os.path.join(dir_, pattern))
        csv_files.extend(files)
    return csv_files


def get_csv_dump_path(country, dump_directory, paths_cache={}):
    file_path = paths_cache.get(country)
    if not file_path:
        file_path = os.path.join(
            dump_directory,
            country.lower() + ".csv"
        )
        paths_cache[country] = file_path
    return file_path
