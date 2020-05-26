# Census Data
This directory handles preprocessing of 2010 census population data at the census block level.

## src
Python scripts for preprocessing the data.

### census_data_preprocess.py
Script to process the census block data by county. Not related to boundary data yet.

### block_to_precinct.py
Script to match census block level data to precincts using boundary data for both. This script uses the data created by the census_data_preprocess script.

### Python Libraries
shapely, pandas

## raw_data
Raw 2010 census population and boundary data. This is a local directory where I stored data found at the below source.

### Population Data
https://factfinder.census.gov/faces/affhelp/jsf/pages/metadata.xhtml?lang=en&type=table&id=table.en.DEC_10_DP_DPDP1#main_content

### Boundary Data
https://www2.census.gov/geo/tiger/TIGER2010BLKPOPHU/
