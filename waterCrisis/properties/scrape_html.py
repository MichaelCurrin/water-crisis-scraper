# -*- coding: utf-8 -*-
"""
Scrape HTML application file.

Read a configured CSV file of suburbs and province metadata which have been
scraped from the property24.com website, but exit if it does not exist yet
(this check is handled within the config script). For each row in the CSV,
fetch HTML for the given URI then write out a text file with an appropriate
name. No processing of the HTML is done in this script.

TODO: Add a command-line flag to force writing over existing files instead of
skipping.
TODO: Consider quiet mode flag to only print when storing, so that the
skipping lines do not take up so much space. This is more important when
testing than when running the first time each day.
TODO: Print aggregate counts rather than individual line, especially when
doing the whole country.
TODO: A configuration for which provinces to get e.g. only western cape. Or
to switch between all data and province only data, since the detail is not
necessary perhaps in all provinces.
"""
import csv
import datetime
import requests
import os
import time

import config


def main():
    """Fetch and write out HTML files around property values.

    @return: None
    @throws: AssertionError
    """
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

            # Get all province data, but suburb data for one province only.
            if (row['area_type'] == 'suburb' and
                    row['parent_name'] != 'western-cape'):
                continue

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
