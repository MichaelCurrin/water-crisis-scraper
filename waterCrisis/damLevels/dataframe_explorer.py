#!/usr/bin/env python3
"""Dataframe explorer application file.

Use an import script to parse the input CSV to a dict and then use
pandas here to parse it to a DataFrame.

No CSV is written out in this process. A benefit of a DataFrame is that it
can be used to raise an error on any duplicate index values.

Some useful commands:
df.columns
df.head()
df.dtypes

# The None values in calc columns cause the column data type to be
# object instead of float, therefore describe values are not shown.
# TODO: Consider how to force column to float and handle None / NaN.
df.describe()
"""
import pandas

from csv_parser import process_input_csv


processed_input_data = process_input_csv()

df = pandas.DataFrame(processed_input_data)
df = df.set_index('Date', verify_integrity=True)
df.index = pandas.to_datetime(df.index)
