#!/bin/bash
# Use curl to fetch HTML pages and store locally. This should be run daily.
#
# TODO: Set instructions for this file and use crontab or cron.daily in
# docs when ready.
# Note no extension.
#   ln -s path/to/scrape_pages_with_curl.sh /etc/cron.daily/scrape_pages_with_curl
# Consider where output should go in project. Top level var, not tools or
# the python package var.
#
# Crontab is not reliable because it requires the machine to be awake for
# network access. But cron.daily will run whenver the machine is awake,
# but then must receive argument for user (sent to this script) or be set to
# run for the user. Consider changing active user and changing directory.
#

# News

URI='https://www.news24.com/SouthAfrica/water_crisis'
TODAY=$(date +'%Y-%m-%d')

OUTPATH="/home/michael/Scripts/water_scrape/html/news24_water_crisis_$TODAY.html"
echo $OUTPATH
curl $URI > $OUTPATH


# Properties

URI='https://www.property24.com/property-values/western-cape/9'
OUTPATH="/home/michael/Scripts/water_scrape/html/property_24_western_cape_$TODAY.html"
echo $OUTPATH
curl $URI > $OUTPATH

URI='https://www.property24.com/property-values/cape-town/western-cape/432'
OUTPATH="/home/michael/Scripts/water_scrape/html/property_24_cape_town_$TODAY.html"
echo $OUTPATH
curl $URI > $OUTPATH

sudo chown michael:michael /home/michael/Scripts/water_scrape/html/*
