![FBB_Logo](https://firmbackbone.nl/wp-content/uploads/sites/694/2025/03/FBB-logo-wide.png)

**[FIRMBACKBONE](https://firmbackbone.nl)** is an organically growing longitudinal data-infrastructure with information on Dutch companies for scientific research and education. Once it is ready, it will become available for researchers and students affiliated with Dutch member universities through the Open Data Infrastructure for Social Science and Economic Innovations ([ODISSEI](https://odissei-data.nl/nl/)). FIRMBACKBONE is an initiative of Utrecht University ([UU](https://www.uu.nl/en)) and the Vrije Universiteit Amsterdam ([VU Amsterdam](https://vu.nl/en)) funded by the Platform Digital Infrastructure-Social Sciences and Humanities ([PDI-SSH](https://pdi-ssh.nl/en/front-page/)) for the period 2020-2025.

## XBRL Files Extractor

A tool for extracting XBRL data from compressed archives. It automates file extraction, parses key financial data, and saves it in a structured format (currently .csv) for analysis. Configurable via a settings file, it supports logging and organized data storage.

### Table of Contents

1. [Run](#run)
2. [Config](#config)
3. [Structure](#structure)

### Run

The environment can be created either from the ```environment.yml``` file or by manually installing packages from ```requirements.txt```. Then just run ```main.py```. Don't forget to add a config file to suit your needs.

### Config

Program can be adjusted using the ```conf.py``` file. Most important fields to edit are:

- ```'logger': 'level'```:        logging level - *DEBUG=10, INFO=20, WARN=30, ERROR=40*
- ```'data': 'zip_path'```:       path to the folder containing the zip files to be extracted
- ```'data': 'dest_path'```:      path to the desired folder for saving extracted XBRL files
- ```'base_columns'```:           list of fields to extract from xbrl and their names in the final table (same as field if empty)
- ```'balancesheet_columns'```:   list of groups with list of columns assigned to this group, if column is not in any list, given group is ***others***

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
