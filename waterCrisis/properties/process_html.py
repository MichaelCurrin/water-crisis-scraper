#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Process HTML application file.

Read property values for all HTML files in the configured directory,
extract and process values, then write out to a single CSV. The CSV
have data for all area and date read in and will replace any existing file.
"""
import csv
import glob
import os

from bs4 import BeautifulSoup

import config


def main():
    """"Read and parse HTML files then write out a CSV of processed data."""
    html_paths = glob.glob(
        os.path.join(config.HTML_OUT_DIR, "*")
    )

    # Used to build a list of dict objects, which can be written out as rows
    # in a single CSV.
    property_out_data = []

    # For debugging, keep track of files which have no results data data,
    # or possibly had a format not expected by the parsing logic which then
    # needs to be adjusted. This list should have relatively few items in it.
    empty_result_pages = []

    print("Extracting data from {} HTML files.".format(len(html_paths)))

    for f_path in html_paths:
        filename = os.path.basename(f_path)
        metadata = os.path.splitext(filename)[0]
        area_type, parent_name, name, area_id, date = metadata.split("|")

        with open(f_path) as f_in:
            text = f_in.read()
            soup = BeautifulSoup(text, 'html.parser')

            description = soup.find("div", attrs={'class':"col-xs-11"})
            first_paragraph = description.find("p")

            if first_paragraph:
                span_tags = first_paragraph.find_all("span")

                # If the HTML layout on the pages ever changes, this will
                # produce the alert so that parsing logic can be adjusted.
                assert len(span_tags) == 4, (
                    "Expected exactly 4 span tags within first p tag but"
                    " got: {count}."
                    "\n{tags}"
                    "\n{f_name}".format(
                        count=len(span_tags),
                        tags=span_tags,
                        f_name=filename
                    )
                )

                # The average price in Rands of properties in this area.
                price_str = span_tags[1].text
                assert price_str.startswith("R "), "Expected span tag to be a"\
                    " value in Rands. Check the source and parser. Value: {}"\
                    .format(span_tags[1])
                # The thousands separator used in HTML is '&#160;' and
                # BeautifulSoup converts this to '\xa0', which prints as a
                # space character.
                price = int(price_str[2:].replace("\xa0", ""))

                # The count of properties listed in this area.
                property_count = int(span_tags[2].text)
            else:
                empty_result_pages.append(filename)
                price = None
                property_count = None

            property_out_data.append({
                'Date': date,
                'Area Type': area_type,
                'Parent': parent_name,
                'Name': name,
                'Ave Price': price,
                'Property Count': property_count
            })

    print("Processed data for {} filenames.".format(len(property_out_data)))
    print("No data to process for {} filenames.".format(
            len(empty_result_pages)
        )
    )

    fieldnames = ['Date', 'Area Type', 'Parent', 'Name', 'Ave Price',
                  'Property Count']
    print("Writing data to: {}... ".format(
        config.DATA_CSV_PATH
        ),
        end=""
    )
    with open(config.DATA_CSV_PATH, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        property_out_data.sort(
            key=lambda x: (x['Date'], x['Area Type'], x['Parent'], x['Name'])
        )
        writer.writerows(property_out_data)
    print("Done.")


if __name__ == '__main__':
    main()
