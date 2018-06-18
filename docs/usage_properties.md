# Usage - Properties


## Handle property data

Follow these commands to fetch and store property data across South Africa from the property24 website and write out to a CSV.

```bash
$ cd path/to/repo
$ source venv/bin/activate
$ cd waterCrisis/properties
```

### 1. Prepare metadata

Run this once-off to generate a CSV of location metadata. This command fetches data for each of the provinces, so only takes a few seconds. The output includes the province and city hierarchy as well as the URI for the row.

```bash
$ ./prepare_metadata.py
Fetching data for: north-west...
Fetching data for: gauteng...
Fetching data for: northern-cape...
Fetching data for: free-state...
Fetching data for: mpumalanga...
Fetching data for: western-cape...
Fetching data for: eastern-cape...
Fetching data for: kwazulu-natal...
Fetching data for: limpopo...
Parsing webpage paths
Writing to: /home/michael/repos/water_crisis_scraper/waterCrisis/properties/var/metadata.csv
```

Now use the metadata CSV generated above to request and download HTML pages for each location and save each using current day's date in the [unprocessed_html](waterCrisis/properties/var/unprocessed_html) directory. If a file exists for a location for the current data, that location is ignored. The locations are limited by what is set in the config file. This command be run daily in order to give a continuous series of data. It takes a few minutes.


### 2. Scrape HTML

```bash
$ ./scrape_html.py
Processing: south-africa | eastern-cape ... 
Processing: south-africa | free-state ... 
Processing: south-africa | gauteng ... 
Processing: south-africa | kwazulu-natal ... 
Processing: south-africa | limpopo ... 
Processing: south-africa | mpumalanga ... 
Processing: south-africa | north-west ... 
Processing: south-africa | northern-cape ... 

...

Processing: western-cape | wellington ...
Processing: western-cape | wilderness ...
Processing: western-cape | witsand ...
Processing: western-cape | wolseley ...
Processing: western-cape | worcester ...
Processing: western-cape | yzerfontein ...

Processed: 702
Skipped: 0
Errors: 0
```

### 3. Process HTML

Go through all HTML files in the [unprocessed_html](/waterCrisis/properties/var/unprocessed_html) directory, extract the property value and count for each and then write out all results to a single CSV file in the [var](/waterCrisis/properties/var) directory, overwriting any existing file. If new HTML files have been added to the [unprocessed_html](/waterCrisis/properties/var/unprocessed_html) directory, then this command should be run to create an updated CSV with more data.

```bash
$ ./process_html.py
Extracting data from 1550 HTML files...
Processed data for 1550 filenames.
No data to process for 158 filenames.
 1. suburb|eastern-cape|jamestown|242|2018-05-28.html
 2. suburb|eastern-cape|seymour|257|2018-06-18.html
 3. suburb|gauteng|muldersdrif|2467|2018-05-28.html
 4. suburb|northern-cape|windsorton|513|2018-05-28.html
 5. suburb|kwazulu-natal|izinqolweni|869|2018-05-28.html
 6. suburb|gauteng|nokeng-tsa-taemane|683|2018-06-18.html
 7. suburb|gauteng|roodeplaat|684|2018-06-18.html

 ...

 157. suburb|eastern-cape|addo|442|2018-05-28.html
 158. suburb|mpumalanga|kwaggafontein|2517|2018-06-18.html
Writing to: /home/michael/repos/water_crisis_scraper/waterCrisis/properties/var/processed_data.csv
```

### Future development

TODO: It is inefficient for storage and processing to keep all the HTML files in that directory. If this becomes an issue, look at moving HTML files once they have been processed and then compress them. Or delete them. However, then data needs to be append to the CSV. This could be handled in pandas and written out as a pickled dataframe.
