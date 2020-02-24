# Election Results
This directory handles preprocessing of Election data for the 2016 and 2018 general elections.

## raw_data
Raw election data for Arizona, Ohio, and Wisconsin.

### Arizona
This directory is split up by county. Each folder refers to a county and holds precinct level data for that county. There are inconsistencies in the file formats across counties.

### Ohio
This directory contains the data in excel worksheet format.

### Wisconsin
This directory contains the data in excel worksheet format. There are seperate files for the congressional and presidential 2016 results.

## src
Python scripts for preprocessing the data

### Python Libraries
pandas, xlrd, xlwt
