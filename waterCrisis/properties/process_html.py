#!/usr/bin/env python3
"""
Process HTML application file.

Read property values for all HTML files in the configured directory,
extract and process values, then write out to a single CSV, writing over
any existing file. The CSV will have data for all areas and dates which
were read in.
"""
import csv
import glob
import os

from bs4 import BeautifulSoup

import config


def parse_property_stats(html):
    """Parse HTML to extract property stats and ignore the rest of the content.

    @param html: HTML text to parse as a single string.

    @return avg_price: Average price in Rands for properties at the location.
    @return property_count: The count of properties listed for sale in the
        location.
    """
    soup = BeautifulSoup(html, 'html.parser')

    description = soup.find("div", attrs={'class': "col-xs-11"})
    first_paragraph = description.find("p")

    if first_paragraph:
        span_tags = first_paragraph.find_all("span")

        # If the HTML layout on the pages ever changes, this will
        # produce the alert so that parsing logic can be adjusted.
        assert len(span_tags) == 4, (
            "Expected exactly 4 span tags within first <p> tag but"
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
        avg_price = int(price_str[2:].replace("\xa0", ""))

        property_count = int(span_tags[2].text)
    else:
        avg_price = None
        property_count = None

    return avg_price, property_count


def main():
    """"Read and parse HTML files then write out a CSV of processed data.

    Expect filenames in one of two styles.
    - A) The project's style, as set in scrape_html.py script.
        e.g. 'suburb|northern-cape|marydale|539|2018-02-09.html'
    - B) A bash script style using a cURL request as in the project's
        tools/scrape_pages_with_curl.sh script.
        e.g. 'property_24_western_cape_2018-05-31.html'
        e.g. 'property_24_cape_town_2018-05-13.html'

    TODO: Add input for alternative HTML directory.
    TODO: Manually parse the WC and CT possibilities, with a separate
        function. Area ID can be ignored.

    @return: None
    """
    html_paths = glob.glob(
        os.path.join(config.HTML_OUT_DIR, "*")
    )

    # Used to build a list of dict objects, which can be written out as rows
    # in a single CSV.
    property_out_data = []

    # For debugging, keep track of files which have no results data,
    # or possibly had a format not expected by the parsing logic which then
    # needs to be adjusted. This list should have relatively few items in it.
    # If the site is under maintenance, the data might be missing for a lot
    # of pages.
    # TODO: Identify the reason and show the label on output.
    empty_result_pages = []

    print("Extracting data from {} HTML files".format(len(html_paths)))

    for f_path in html_paths:
        with open(f_path) as f_in:
            html = f_in.read()
        avg_price, property_count = parse_property_stats(html)

        filename = os.path.basename(f_path)
        metadata = os.path.splitext(filename)[0]
        area_type, parent_name, name, area_id, date = metadata.split("|")

        property_out_data.append(
            {
                'Date': date,
                'Area Type': area_type,
                'Parent': parent_name,
                'Name': name,
                'Ave Price': avg_price,
                'Property Count': property_count
            }
        )

        if avg_price is None:
            empty_result_pages.append(filename)
        print("#", end=" ", flush=True)

    print("\nProcessed data for {} filenames.".format(len(property_out_data)))

    print("No data to process for {} filenames.".format(
          len(empty_result_pages)))
    for i, filename in enumerate(empty_result_pages):
        print(" {index:d}. {filename}".format(
            index=i+1,
            filename=filename
        ))

    fieldnames = ['Date', 'Area Type', 'Parent', 'Name', 'Ave Price',
                  'Property Count']
    print("Writing to: {}".format(config.DATA_CSV_PATH))
    with open(config.DATA_CSV_PATH, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        property_out_data.sort(
            key=lambda x: (x['Date'], x['Area Type'], x['Parent'], x['Name'])
        )
        writer.writerows(property_out_data)


if __name__ == '__main__':
    main()
