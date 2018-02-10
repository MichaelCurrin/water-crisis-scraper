# Water Crisis
>Scrape and explore data related to Cape Town's water crisis.


## Data sources


### Dam Levels

The **[dam_levels module](waterCrisis/dam_levels)** handles government data on historical and current dam levels in the Western Cape.

A CSV of dam levels from 2012 to 2018 is obtainable at no cost from the [Dam levels data set](https://web1.capetown.gov.za/web1/opendataportal/DatasetDetail?DatasetName=Dam+levels) page, hosted on the _City of Cape Town Open Data Portal_.

Disclaimer:

>This site provides products or services using data that has been modified for use from its original source, [www.capetown.gov.za](http://www.capetown.gov.za/), the official website of the City of Cape Town. The City of Cape Town makes no claims as to the content, accuracy, timeliness, or completeness of any of the data provided at this site.
The data provided at this site is subject to change at any time. It is understood that the data provided at this site is being used at one’s own risk.


### Properties

The **[properties module](waterCrisis/properties)** processes average property price data for South Africa, sourced from the [property24 website](https://www.property24.com/) site.

Here is the starting reference point on the website for those values: [property values in South Africa](https://www.property24.com/property-values). That webpage allows going down to province or suburb levels and getting the average value and count of properties for that area.

For example:

> **Property values in Western Cape**
> Currently the average price of properties in Western Cape is R 3 425 228. There are currently 65890 properties on the market in Western Cape.

The values are visible in the browser and accessible when parsing the HTML. They are assumed to be current, but there is no indication as to how frequently they are updated.

This section of the project deals with regulary saving the raw HTML files to the unprocessed_html directory and then later extracting values from the local files when required. It is expensive to keep these files about 700 files covering the whole country is about 50MB. An alternative process could be to fetch, process and discard the HTML data. Or to get suburb data for one province of interest but only top-level data for other provinces. This means appending to a CSV and not overwriting it.

Note that included data here is limited to the point of view of [property24 website](https://www.property24.com/) listings, but should still be useful for analysis.

The website also offers more granular data, including visualisations and history, such as [Cape Town City Centre property trends](https://www.property24.com/cape-town/cape-town-city-centre/property-trends/9138). This is not handled in this project though.
