# Election Results
This directory handles preprocessing of Election data for the 2016 and 2018 general elections.

## raw_data
Raw election data for Arizona, Ohio, and Wisconsin. This is a local directory where I stored data found at the below sources.

### Arizona
This directory is split up by county. Each folder refers to a county and holds precinct level data for that county. There are inconsistencies in the file formats across counties(ElectionWare, GEMS, OpenElect, WinEDS).

#### Congressional/Pres election 2016:
https://apps.azsos.gov/results/2016/General/

#### Congressional election 2018:
https://azsos.gov/precinct-level-results-county-2018-general-election

### Ohio
This directory contains the data in excel worksheet format.

#### Congressional/Pres election 2016:
https://www.sos.state.oh.us/globalassets/elections/2016/gen/precinct.xlsx

#### Congressional election 2018:
https://www.sos.state.oh.us/globalassets/elections/2018/gen/2018-11-06_statewideprecinct_miami.xlsx


### Wisconsin
This directory contains the data in excel worksheet format for county level data. There is precinct level data from MIT dataware.

#### Con 2016:
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PSKDUJ

#### Pres 2016:
https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/LYWX3D

#### Con 2018:
https://github.com/MEDSL/2018-elections-official/blob/master/precinct_2018.zip


## src
Python scripts for preprocessing the data. Further cleaning of precinct names were done manually to better match the precinct names in the boundary files.

### Python Libraries
pandas
