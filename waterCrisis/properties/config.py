# -*- coding: utf-8 -*-
"""
Configuration file for the properties module.
"""
import os


def _get_file_paths():
    """Build and return configured paths for reading and writing files.

    @return: Tuple of path to the following locations:
        - var directory.
        - CSV file to write area metadata.
        - directory to write out HTML files.
        - CSV file to write processed area data.
    """
    var_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "var"))
    assert os.access(var_path, os.W_OK), \
        "Unable to write to var directory: {}".format(var_path)

    metadata_csv_path = os.path.join(var_path, "metadata.csv")
    html_out_dir = os.path.join(var_path, "unprocessed_html")
    data_csv_path = os.path.join(var_path, "processed_data.csv")

    return var_path, metadata_csv_path, html_out_dir, data_csv_path


### Paths

VAR_PATH, METADATA_CSV_PATH, HTML_OUT_DIR, DATA_CSV_PATH = _get_file_paths()


### Locations

HOST_DOMAIN = "https://www.property24.com"
PROVINCE_PATHS = {
    'western-cape': "/property-values/western-cape/9",
    'gauteng': "/property-values/gauteng/1",
    'kwazulu-natal': "/property-values/kwazulu-natal/2",
    'free-state': "/property-values/free-state/3",
    'mpumalanga': "/property-values/mpumalanga/5",
    'eastern-cape': "/property-values/eastern-cape/7",
    'north-west': "/property-values/north-west/6",
    'limpopo': "/property-values/limpopo/14",
    'northern-cape': "/property-values/northern-cape/8"
}
# Names of provinces for which suburb-level data should be fetched.
# Set to [] for none, or list(PROVINCE_PATHS.keys()) for all.
SUBURB_DETAIL_REQUIRED = ['western-cape']
SUBURB_DETAIL_REQUIRED = list(PROVINCE_PATHS.keys())

### Requests

# Number of seconds to wait for response before aborting.
REQUEST_TIMEOUT = 5
# Fake a browser visit to avoid getting blocked as a scraper.
REQUEST_HEADERS = {
    'Accept': "text/html,application/xhtml+xml,application/xml;"
              "q=0.9,image/webp,*/*;q=0.8",
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
}
# Number of seconds to wait between requests to avoid being blocked.
# Set 0.0 to not wait.
REQUEST_SPACING = 0.5

# If True, when scraping HTML then skip any local files which already exist,
# otherwise do the request and overwrite the file. Overwriting should only
# be necessary if there was an issue in the existing fetch and the files
# must be replaced with better ones. Or for development and testing purposes.
SKIP_EXISTING = True

# If True, be more verbose and print out a line when an item is skipped.
SHOW_SKIPPED = False
