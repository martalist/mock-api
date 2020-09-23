#!/usr/bin/env python

import os, sys
import dataset
from dbfread import DBF
import time

def get_dbf_files(input_dir):
    result = []
    for root, dirname, filenames in os.walk(input_dir):
        for fn in filenames:
            if fn.endswith(".dbf"):
                result.append(os.path.join(root, fn))
    return result

def convert_to_sql(filenames, database):
    table = database['PointData']
    for fn in filenames:
        start = time.time()
        print(f'Converting {fn} to sqlite')
        for record in DBF(fn, lowernames=True):
            table.insert(record)
        duration = time.time() - start
        print(f'Converted {fn} to sqlite in {duration} seconds')

if __name__ == "__main__":
    input_dir = os.getcwd()
    output_dir = os.path.join(input_dir, "output")

    dbf_files = get_dbf_files(input_dir)

    database = dataset.connect('sqlite:///maritimeData.sqlite')
    convert_to_sql(dbf_files, database)
    print("Done")
