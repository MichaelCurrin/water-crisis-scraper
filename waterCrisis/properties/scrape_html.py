# -*- coding: utf-8 -*-
"""Scrape HTML application file.

Read a configured CSV file of suburbs and province metadata which have been
scraped from the property24.com website. For each row in the CSV, fetch HTML
for the given URI then write out a text file with an appropriate name.
No processing of the HTML is done here.

The filenames include metadata attributes to make it easy identify what
area the HTML is for, or to view and sort a list of filesnames. The filenames
include the date they were generated, so that a history of files for the
same location can be built up, to be parsed later. Note that an existing
HTML file will be skipped if one already exists for the current date.
This is useful so that if the script stops partway through processing,
it can pick up when it left off when it restarts.

TODO: Add a command-line flag to force writing over existing files instead of
skipping.
TODO: Consider quiet mode flag to only print when storing, so that the
skipping lines do not take up so much space. This is more important when
testing than when running the first time each day.
"""
import csv
import datetime
import requests
import os
import time

import config


def main():
    """Main function to fetch and write out property data HTML files."""
    today = datetime.date.today()

    with open(config.METADATA_CSV_PATH) as f_in:
        reader = csv.DictReader(f_in)

        for row in reader:
            out_name = "{area_type}|{parent_name}|{name}|{area_id}|{date}"\
                ".html".format(
                    area_type=row['area_type'],
                    parent_name=row['parent_name'],
                    name=row['name'],
                    area_id=row['area_id'],
                    date=str(today)
                )
            out_path = os.path.join(config.HTML_OUT_DIR, out_name)

            if os.path.exists(out_path):
                print("Skipping: {name} ({parent})".format(
                        name=row['name'],
                        parent=row['parent_name']
                    )
                )
            else:
                print("Processing: {name} ({parent})... ".format(
                        name=row['name'],
                        parent=row['parent_name']
                    ),
                    end=''
                )
                resp = requests.get(
                    row['uri'],
                    timeout=config.REQUEST_TIMEOUT,
                    headers=config.REQUEST_HEADERS
                )

                if resp.status_code == 200:
                    with open(out_path, 'w') as f_out:
                        f_out.writelines(resp.text)
                    print("Done.")
                    # Wait between requests, to avoid being possibly
                    # blocked by the server for doing requests too frequently.
                    time.sleep(config.REQUEST_SPACING)
                else:
                    msg = "Request for HTML file failed."\
                        "\n  {code} {reason}"\
                        "\n  {uri}".format(
                        code=resp.status_code,
                        reason=resp.reason,
                        uri=row['uri']
                    )
                    raise AssertionError(msg)


if __name__ == '__main__':
    main()
