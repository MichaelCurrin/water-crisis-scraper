# -*- coding: utf-8 -*-
"""
Scrape HTML application file.

Read a configured CSV file of suburbs and province metadata which have been
scraped from the property24.com website, but exit if it does not exist yet
(this check is handled within the config script). For each row in the CSV,
fetch HTML for the given URI then write out a text file with an appropriate
name. No processing of the HTML is done in this script.

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

    Use requests.Session to keep a connection open to the domain and get a
    performance benefit, as per the documentation here:
        http://docs.python-requests.org/en/master/user/advanced/

    @return: None
    @throws: AssertionError
    """
    today = datetime.date.today()
    session = requests.Session()
    processed = skipped = errors = 0

    with open(config.METADATA_CSV_PATH) as f_in:
        reader = csv.DictReader(f_in)

        try:
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

                # For suburbs, only fetch those which match configured provinces.
                if (row['area_type'] == 'suburb' and
                        row['parent_name'] not in config.SUBURB_DETAIL_REQUIRED):
                    continue

                if config.SKIP_EXISTING and os.path.exists(out_path):
                    if config.SHOW_SKIPPED:
                        print("Skipping: {parent} | {name}".format(
                                name=row['name'],
                                parent=row['parent_name']
                            )
                        )
                    skipped += 1
                else:
                    print("Processing: {parent} | {name} ... ".format(
                            name=row['name'],
                            parent=row['parent_name']
                        ),
                    )
                    resp = session.get(
                        row['uri'],
                        timeout=config.REQUEST_TIMEOUT,
                        headers=config.REQUEST_HEADERS
                    )

                    if resp.status_code == 200:
                        with open(out_path, 'w') as f_out:
                            f_out.writelines(resp.text)
                        # Wait between requests, to avoid being possibly
                        # blocked by the server for doing requests too frequently.
                        time.sleep(config.REQUEST_SPACING)
                        processed += 1
                    else:
                        error = dict(
                            code=resp.status_code,
                            reason=resp.reason,
                            uri=row['uri']
                        )
                        print("Error: {code} {reason} {uri}".format(**error))
                        errors += 1
        finally:
            print("\nProcessed: {}".format(processed))
            print("Skipped: {}".format(skipped))
            print("Errors: {}".format(errors))


if __name__ == '__main__':
    main()
