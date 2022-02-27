#!/bin/bash -e
# Fetch HTML pages and store locally.
#
# A simple script which use `curl` to save just a few pages specified manually,
# if the need is just to get minimal data. This script should be run daily.
#
# It could be more efficient to check status as 200 before writing but then
# possibly do in python for ease. The idea is a simple bash script.

write_data() {
  if [ $# -ne 2 ]; then
    printf "Expected 2 arguments, got: %d\n" $#
    exit 1
  fi

  URI="$1"
  OUT_PATH="$2"

  echo $(basename "$OUT_PATH")

  if [ -s "$OUT_PATH" ]; then
    echo ' skip existing non-empty file'
  else
    if [ -e "$OUT_PATH" ]; then
      echo ' overwriting empty file'
    else
      echo ' creating file'
    fi
    curl "$URI" >"$OUT_PATH"
  fi

  echo
}

PROJECT_ROOT=$(cd $(dirname $0) && git rev-parse --show-toplevel)
OUT_DIR=$PROJECT_ROOT/waterCrisis/properties/var/unprocessed_html

TODAY=$(date +'%Y-%m-%d')

WC_IN='https://www.property24.com/property-values/western-cape/9'
CT_IN='https://www.property24.com/property-values/cape-town/western-cape/432'

WC_OUT="$OUT_DIR/property_24_western_cape_$TODAY.html"
CT_OUT="$OUT_DIR/property_24_cape_town_$TODAY.html"

write_data "$WC_IN" "$WC_OUT"
write_data "$CT_IN" "$CT_OUT"
