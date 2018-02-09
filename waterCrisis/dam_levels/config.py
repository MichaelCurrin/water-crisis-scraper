"""Configuration file for the dam_levels module."""
import os


def _get_capacity():
    """Return constant values for dam level capacities.

    Storage capacity values are measured in million cubic metres
    i.e. Megalitres or Ml.

    Source: https://en.wikipedia.org/wiki/Western_Cape_Water_Supply_System

    @return capacity: Dict object containing maximum capacities of Western
        Cape dams. Includes aggregate values for small dams, big six dams
        and all dams.
    """
    big_six_capacity = {
        'Theewaterskloof': 480188,
        'Wemmershoek': 58644,
        'Steensbras Lower': 33517,
        'Steenbras Upper': 31757,
        'Voëlvlei': 164095,
        'Berg River': 130010,
    }

    small_capacity = {
        'Hely-Hutchinson': 925,
        'Woodhead': 954,
        'Victoria': 128,
        'De Villiers': 243,
        'Kleinplaats': 1368,
        'Lewis Gay': 182,
        'Land-en-Zeezicht': 451,
    }

    capacity = {**big_six_capacity, **small_capacity}

    capacity['Big Six Dams'] = sum(big_six_capacity.values())
    capacity['Small Dams'] = sum(small_capacity.values())
    capacity['All Dams'] = capacity['Small Dams'] + capacity['Big Six Dams']

    return capacity


def _get_csv_details(csv_in_filename, csv_out_filename):
    """Return tuple of configured CSV input and output details.

    Also verifies that the process has access to read the input file
    and write to the output file.

    The CSV input file is expected to be a download of the file
    "Dam levels update 2012-2018.csv" on this webpage:
        https://web1.capetown.gov.za/web1/opendataportal/DatasetDetail?DatasetName=Dam+levels
    The file is not directly downloadable with cURL, as it requires a
    headless browser to execute the JavaScript.

    @param csv_in_filename: Name of input CSV file to build full path for.
    @param csv_out_filename: Name of output CSV file to build full path for.

    @return: Tuple of configured CSV input and output paths.
    """
    var_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'var'))
    csv_in_path = os.path.join(var_dir, csv_in_filename)
    csv_out_path = os.path.join(var_dir, csv_out_filename)

    assert os.access(csv_in_path, os.R_OK), \
        "Unable to read CSV path: {}".format(csv_in_path)

    csv_out_dir = os.path.dirname(csv_out_path)
    assert os.access(csv_out_dir, os.W_OK), \
        "Unable to write to CSV out dir: {}".format(csv_out_dir)

    return csv_in_path, csv_out_path


CAPACITY = _get_capacity()

# Encoding required to avoid error on reading the input CSV. Values of None
# or 'utf-8', will result in an error decoding byte `0xcb`. This is around the
# VOËLVLEI label.
# >>> chr(0xcb)
# 'Ë'
# Note that this is only needed for input, as the default encoding was
# found to be safe for writing out accented characters.
CSV_IN_ENCODING = "latin-1"

CSV_IN_PATH, CSV_OUT_PATH = _get_csv_details(
    csv_in_filename="Dam levels update 2012-2018.csv",
    csv_out_filename="dam_levels_cleaned.csv"
)
