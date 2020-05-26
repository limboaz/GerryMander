# Boundary Data
This directory handles preprocessing of boundary data from data.gov and identifying boundary related suspected errors

## src
Python scripts for preprocessing the data.

### convert_shp
Directory with script used to convert shp files to GeoJSON files

### district_process
Script to process congressional district boundary data. Convert to csv in db format

### precinct_process.py
Script to process precinct boundary data. Convert to csv in db format.

 - Match precicnt to congressional district
 - Match fip code to county name
 - Identify unassigned area
 - Identify multipolygons
 - Identify enclosed precincts
 - Identify overlapping precicnts
 - Identify election errors
 - Create csv files matching db format for the appropriate table (Precicnt, DataErrors, BoundaryErrors)
 
### combine_BDY
Script to combine the precincts that had initial district match with those that were matched after inital together for all states.

### Python Libraries
shapely, pandas, fiona
