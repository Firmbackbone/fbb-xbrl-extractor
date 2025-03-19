# FIRMBACKBONE

## XBRL Files Extractor

...

### Table of Contents

1. [Run](#run)
2. [Config](#config)
3. [Structure](#structure)

### Run

...

### Config

Program can be adjusted using the ```conf.py``` file. Most important fields to edit are:

- ```'logger': 'level'```:        logging level - *DEBUG=10, INFO=20, WARN=30, ERROR=40*
- ```'data': 'zip_path'```:       path to the folder containing the zip files to be extracted
- ```'data': 'dest_path'```:      path to the desired folder for saving extracted XBRL files
- ```'base_columns'```:           list of fields to extract from xbrl and their names in the final table (same as field if empty)
- ```'balancesheet_columns'```:   list of groups with list of columns assigned to this group, if column is not in any list, given group is *others*

### Structure

```
├──  data                     - placeholder directory for storing data
│
├──  logs                     - if logs enabled they are stored there
│
├──  outputs                  - output csv files goes there
│
├──  src
│    └──  extractors.py       - extracting xbrls from zip files
│    └──  parsers.py          - parsing xbrls into structured data
│    └──  utils.py            - some helpful functions
│
└── conf.py                   - config file
└── assets_analysis.ipynb     - xbrl fields and values analysis 
└── main.py                   - main program loop

```
