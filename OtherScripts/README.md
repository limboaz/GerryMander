# Other Scripts
This directory handles preprocessing of neighbors, cleaning data

## src
Python scrpits

### neighbors
Script to find precinct neighbors that share a preimeter of at least 500 ft

### create district
Script to create a congressional district for WI called -1 so that the districts covered the whole state

### combine errors
Script to combine all the errors identified into one file

### isolate duplicates
Script to find all the precicnts across all three states (same state_county_precinct). We found 8. I manually renamed their unique ID to state_county_precinct(2).

### add state id
Script to add state id to errors identified in preprocessing. Not a field we needed in earlier development.

### Python Libraries
shapely, pandas
