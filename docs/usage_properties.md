# Usage - Properties

This section describes tools to scrape property data from _Property24_ site and store as HTML, using Bash or Python. And a tool to parse the stored HTMl and generate a CSV report.

Use either [Light Scraping](#light-scraping) or [Deep Scraping](#deep-scraping) and then see the [Process HTML](#process-html) section.

The light tool can easily be run daily as it is not intense in time or storage as scraping data for all areas in South Africa as covered in the next section. If you the deep scraping tool, you will duplicate the 3 files from the light tool.


## Light scraping

Use the project's tool scrape property data for Cape Town and the Western Cape, plus water crisis data from _News24_. These are important for comparisons and because Cape Town experienced a water shortage from about 2008.

The script is [scrape_pages_with_curl.sh](/tools/scrape_pages_with_curl.sh). It will skip over requesting and saving a file if one already exists for the current day.

Use crontab to run the tool several times a day, allowing chances to retry later in the day if if network connection was off or the domain was unreachable. Or use daily cron, which is less forgiving.

### Crontab

Add something like this to your cron file.

```bash
$ crontab -e
```

```
# m     h       dom     mon     dow     command
  30    7-18    *       *       *       <PATH_TO_REPO>/tools/scrape_pages_with_curl.sh
```

### Daily cron

Add a link to the tool in your `cron.daily` directory. Note that the link must not have an extension.

```bash
$ sudo ln -s <PATH_TO_REPO>/scrape_pages_with_curl.sh /etc/cron.daily/scrape_pages_with_curl
```

## Deep Scraping

Follow these commands to fetch and store property data across South Africa from the _Property24_ website and write out to a CSV.

```bash
$ cd <PATH_TO_REPO>
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
Writing to: /.../waterCrisis/properties/var/metadata.csv
```

Now use the metadata CSV generated above to request and download HTML pages for each location and save each using current day's date in the [unprocessed_html](/waterCrisis/properties/var/unprocessed_html) directory. If a file exists for a location for the current data, that location is ignored. The locations are limited by what is set in the config file. This command be run daily in order to give a continuous series of data. It takes a few minutes.


### 2. Scrape HTML

This requires the metadata CSV from the above step to exist.

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

Note that the total fetched count can vary - counts of 625 and 702 have been observed.

### Process HTML

Go through all HTML files in the [unprocessed_html](/waterCrisis/properties/var/unprocessed_html) directory, extract the property value and count for each and then write out all results to a single CSV file in the [var](/waterCrisis/properties/var) directory, overwriting any existing file. If new HTML files have been added to the [unprocessed_html](/waterCrisis/properties/var/unprocessed_html) directory, then this command should be run to create an updated CSV with more data.

```bash
$ ./process_html.py
Extracting data from 1550 HTML files
  10 done
  20 done
  30 done
  40 done
  50 done
  ...
  1540 done
  1550 done
Successfully processed: 1,392.
Failed to process: 158.
   1. suburb|eastern-cape|addo|442|2018-05-28.html (1,283 rows)
   2. suburb|eastern-cape|addo|442|2018-06-18.html (1,283 rows)
   3. suburb|eastern-cape|balfour|256|2018-05-28.html (1,339 rows)
   4. suburb|eastern-cape|balfour|256|2018-06-18.html (1,339 rows)
   5. suburb|eastern-cape|bizana|2481|2018-05-28.html (2,566 rows)
 ...
 157. suburb|western-cape|citrusdal|422|2018-05-26.html (1,320 rows)
 158. suburb|western-cape|citrusdal|422|2018-05-28.html (1,303 rows)
Writing to: /home/michael/repos/water_crisis_scraper/waterCrisis/properties/var/processed_data.csv
```

Optionally specify an alternate directory to read HTML data from.

```bash
$ ./process_html.py --read ~/path/to/html_dir
```

### Future development

TODO: It is inefficient for storage and processing to keep all the HTML files in that directory. If this becomes an issue, look at moving HTML files once they have been processed and then compress them. Or delete them. However, then data needs to be append to the CSV. This could be handled in pandas and written out as a pickled dataframe.
