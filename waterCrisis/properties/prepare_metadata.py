# -*- coding: utf-8 -*-
"""Prepare Metadata application file.

Scrapes attributes of configured areas and writes out their metadata to a CSV.

Reads property24 HTML data for given URLs of provinces in South Africa.
Extract the details of each suburb listed and write out a CSV. The suburbs
and their attributes handled here are expected to be static, so the CSV does
not need to be updated often.

The output could be JSON, but CSV makes it easy to sort and filter the data
in a CSV viewer.
"""
import csv

import requests
from bs4 import BeautifulSoup

import config


def parse_path(path):
    """Extract elements from a path in an expected format and return as a dict.

    @param path: Relative path on the property24 website, for either province
        or suburb values.

    @return: dict object with the following format::
        {
            'area_id': int,
            'area_type': str,
            'parent_name': str,
            'name': str,
            'uri': str
        }
    """
    uri = "".join((config.HOST_DOMAIN, path))

    # Ignore the constant part of the path.
    elements = path.split("/")[2:]

    if len(elements) == 2:
        area_type = 'province'
        parent_name = 'south-africa'
        name, area_id = elements
    elif len(elements) == 3:
        area_type = 'suburb'
        name, parent_name, area_id = elements
    else:
        raise ValueError("Cannot process path: {}".format(path))

    return {
        'area_id': int(area_id),
        'area_type': area_type,
        'parent_name': parent_name,
        'name': name,
        'uri': uri
    }


def main():
    """Main function to prepare property metadata.

    Iterate through paths of configured provinces to fetch the HTML,
    and scrape the href tags. When all provinces are done, write out a single
    CSV file of the metadata for all areas.
    """
    # Relative paths of provinces and suburbs which have been scraped,
    # ignoring duplicates as province paths tend to be repeated on a page
    # because of appearing in droplists.
    paths = set()

    for province_name, province_path in config.PROVINCE_PATHS.items():
        print("Fetching data for: {0}...".format(province_name))
        province_url = "".join((config.HOST_DOMAIN, province_path))
        resp = requests.get(province_url)
        soup = BeautifulSoup(resp.text, 'html.parser')

        for tag in soup.find_all('a'):
            href = tag.get('href')
            if href and href.startswith("/property-values/"):
                paths.update((href,))

    print("Parsing paths...")
    property_data = [parse_path(p) for p in paths]
    property_data = sorted(
        property_data,
        key=lambda x: (x['area_type'], x['parent_name'], x['name'])
    )

    print("Writing CSV file...")
    with open(config.METADATA_CSV_PATH, 'w') as f:
        fieldnames = ['area_id', 'area_type', 'parent_name', 'name', 'uri']
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(property_data)

    print("Done.")


if __name__ == '__main__':
    main()