#!/usr/bin/env python3
"""
Process HTML application file.

Read property values for all HTML files in the configured directory,
extract and process values, then write out to a single CSV, writing over
any existing file. The CSV will have data for all areas and dates which
were read in.
"""
import argparse
import csv
import glob
import os

from bs4 import BeautifulSoup

import config


METADATA_LOOKUP = {
    'western_cape': {
        'parent_name': "south-africa",
        'area_type': "province",
        'name': 'western-cape'
    },
    'cape_town': {
        'parent_name': "western-cape",
        'area_type': "suburb",
        'name': 'cape-town'
    }
}


def parse_curl_metadata(filename):
    """
    Use the details in a curl-generated HTML filename to extract metadata.

    See the project's tools/scrape_pages_with_curl.sh bash script.

    @param filename: The filename of the HTML file, without the extension.
        Note that the filename has underscores but the returned values
        have hyphens.

        Format:
            "property_24_{area}_{date}.html"
        Examples:
            "property_24_western_cape_2018-05-31.html"
            "property_24_cape_town_2018-05-13.html"

        Only those two areas are handled here, using hardcoded rules as the
        bash script is not intended to be used to scale to many locations. The
        other logic for parsing filenames easily covers all areas though.

    @return: Tuple of metadata string values as
        (area_type, parent_name, name, date).
    """
    metadata, _ = os.path.splitext(filename)
    metadata = metadata.replace("property_24_", "")
    name, date = metadata.rsplit("_", 1)

    area_metadata = METADATA_LOOKUP[name]
    area_type = area_metadata['area_type']
    parent_name = area_metadata['parent_name']
    name = area_metadata['name']

    return area_type, parent_name, name, date


def parse_property_stats(html):
    """
    Parse HTML to extract property stats and ignore the rest of the content.

    Note the value description can be missing in the case of a maintenance page.

    @param html: HTML text to parse as a single string. If this is empty
        or does not have the expected paragraph of data, then return None
        values.

    @return tuple
        avg_price: Average price in Rands for properties at the location.
        property_count: The count of properties listed for sale in the
            location.
    """
    avg_price = None
    property_count = None

    if html:
        soup = BeautifulSoup(html, 'html.parser')
        value_description = soup.find("div", attrs={'class': "col-xs-11"})

        if value_description:
            first_paragraph = value_description.find("p")

            if first_paragraph:
                span_tags = first_paragraph.find_all("span")

                # If the HTML layout on the pages ever changes, this will
                # produce the alert so that parsing logic can be adjusted.
                assert len(span_tags) == 4, (
                    "Expected exactly 4 span tags within first <p> tag but"
                    " got: {count}. \n{tags}".format(
                        count=len(span_tags),
                        tags=span_tags,
                    )
                )

                # The average price in Rands of properties in this area.
                price_str = span_tags[1].text
                assert price_str.startswith("R"), "Expected span tag to be a"\
                    " value in Rands. Check the source and parser. Element: {}"\
                    .format(span_tags[1])
                # The value can be 'R xxx' or 'R-xxx', though the negative value may
                # be data on the site. The minus sign is kept when parsing.
                # But remove the thousands separator - in HTML this is '&#160;' and
                # BeautifulSoup converts this to '\xa0' and which prints as a
                # space character in the terminal.
                avg_price = int(price_str[1:].replace("\xa0", ""))
                property_count = int(span_tags[2].text)

    return avg_price, property_count


def parse_html(f_path):
    """
    Parse HTML of a given filename and return processed data and line count.

    @param f_path: Path HTML file to open and parse.

    @return row_data: dict of processed data with the following format:
            {
                'Date': str,
                'Area Type': str,
                'Parent': str,
                'Name': str,
                'Ave Price': int or None,
                'Property Count': int or None
            }
        Or if there is no data in the file to parse because the file is empty
        or in an unexpected structure, return None instead.
    @return filename: Name of HTML, extracted from f_path value.
    @return line_count: int as number of lines in the input text file.
    """
    with open(f_path) as f_in:
        html = f_in.read()

    filename = os.path.basename(f_path)
    line_count = len(html.split("\n")) if html else 0

    # TODO: Refactor the 2nd to be a function or to have the conditional inside
    # a function.
    if filename.startswith("property_24_"):
        area_type, parent_name, name, date = parse_curl_metadata(filename)
    else:
        metadata, _ = os.path.splitext(filename)
        area_type, parent_name, name, _, date = metadata.split("|")

    try:
        avg_price, property_count = parse_property_stats(html)
    except Exception:
        print("\nError parsing file: {}".format(f_path))
        print("Line count: {:,d}".format(line_count))
        raise

    if avg_price is not None:
        row_data = {
            'Date': date,
            'Area Type': area_type,
            'Parent': parent_name,
            'Name': name,
            'Average Price': avg_price,
            'Property Count': property_count
        }
    else:
        row_data = None

    return row_data, filename, line_count


def html_to_csv(html_dir):
    """
    Read and parse HTML files then write out processed data to a single CSV.

    HTML filenames are mostly expected to be in style set in scrape_html.py.
        "{area_type}|{parent_name}|{name}|{area_id}|{date}.html"
    Example:
        "suburb|northern-cape|marydale|539|2018-02-09.html"

    An alternative style is accepted as explained in `parse_curl_metadata`
    function of this script.

    TODO: Two input directories but one output file? Or two output files or
    merge inputs directories?

    @param html_dir: Path to directory of HTML files to parse.

    @return: None
    """
    # dict objects to be written out as CSV rows.
    property_out_data = []
    # Keep track of files which are either empty or have HTML structure
    # which is not expected such as when the site is under maintenance.
    bad_data_pages = []

    assert os.access(html_dir, os.R_OK), \
        "Unable to read directory: {}".format(html_dir)

    print("Finding .html files in directory: {}".format(html_dir))
    html_paths = glob.glob(
        os.path.join(html_dir, "*.html")
    )
    # Ignore unrelated News24 files possibly created with the bash script
    # in the tools directory.
    html_paths = [path for path in html_paths
                  if not os.path.basename(path).startswith("news24_")]
    html_paths.sort()

    print("Extracting data from {} HTML files".format(len(html_paths)))

    success_line_counts = []
    for i, f_path in enumerate(html_paths):
        row_data, filename, line_count = parse_html(f_path)

        if row_data:
            property_out_data.append(row_data)
            success_line_counts.append(line_count)
        else:
            bad_data_pages.append(
                (filename, line_count)
            )
        if (i+1) % 10 == 0:
            print("{:4d} done".format(i+1))

    print("Success")
    print(" - file count: {:,d}".format(len(property_out_data)))
    print(" - average line count: {:2,.1f}".format(
        (sum(success_line_counts)/len(success_line_counts))
    ))
    print(" - max line count: {:,d}".format(max(success_line_counts)))
    print(" - mix line count: {:,d}".format(min(success_line_counts)))

    print("Failed")
    print(" - file count: {:,d}".format(len(bad_data_pages)))
    print(" - items:")
    for i, (filename, line_count) in enumerate(bad_data_pages):
        print("  {index:4d}. {filename} ({line_count:,d} rows)".format(
            index=i+1,
            filename=filename,
            line_count=line_count
        ))

    print("Writing to: {}".format(config.DATA_CSV_PATH))
    fieldnames = ['Date', 'Area Type', 'Parent', 'Name', 'Average Price',
                  'Property Count']
    with open(config.DATA_CSV_PATH, 'w') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        property_out_data.sort(
            key=lambda x: (x['Date'], x['Area Type'], x['Parent'], x['Name'])
        )
        writer.writerows(property_out_data)


def main():
    """
    Command-line function to parse arguments and read and write data.
    """
    parser = argparse.ArgumentParser(description="Process HTML utility."
                                     " Parse HTML files and write out"
                                     " processed data to a single CSV file.")
    parser.add_argument(
        '-r', '--read',
        metavar="DIR_PATH",
        help="Optionally choose a directory to read HTML files from, even"
            " exist outside the project. Omit this option to use the"
            " configured default: {}".format(config.HTML_OUT_DIR)
    )
    args = parser.parse_args()

    html_dir = args.read if args.read else config.HTML_OUT_DIR
    html_to_csv(html_dir)


if __name__ == '__main__':
    main()
