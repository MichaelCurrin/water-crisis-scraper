#!/usr/bin/env python3
"""
Dataframe explorer application file.

Read in the raw input CSV, apply the cleaning logic as in `csv_parser`
and then convert the dict object to a DataFrame, instead of writing to a CSV.
The DataFrame is kept in memory and can be explored easily in iPython.
No data is written out by this script.

A benefit of the DataFrame is that it can be used to raise an error on any
duplicate index values, which have to be solved by updating the cleaning
logic. This was done previously to identify rows in the source CSV which
have irregular date formats or values.

Some useful commands to apply in pandas:
>>> df.columns
>>> df.head()
>>> df.dtypes

The None values in calc columns cause the column data type to be
object instead of float, therefore describe values are missing for those
columns.
TODO: Consider how to force column to float and handle None / NaN.
>>> df.describe()
"""
import pandas

from csv_parser import process_input_csv


processed_input_data = process_input_csv()

df = pandas.DataFrame(processed_input_data)
df = df.set_index('Date', verify_integrity=True)
df.index = pandas.to_datetime(df.index)
