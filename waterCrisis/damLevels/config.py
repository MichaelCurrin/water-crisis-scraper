"""Configuration file for dam CSV parser."""
import os


def getCapacity():
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


CAPACITY = getCapacity()

varDir = os.path.join(os.path.dirname(__file__), 'var')

# Encoding cannot be None or 'utf-8', since then there is an error on decoding
# byte `0xcb`. This is around VOËLVLEI cell.
# >>> chr(0xcb)
# 'Ë'
CSV_IN_ENCODING = 'latin-1'
CSV_IN_PATH = os.path.join(varDir, 'Dam levels update 2012-2018.csv')
CSV_OUT_PATH = os.path.join(varDir, 'dam_levels_cleaned.csv')
