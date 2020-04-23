# match census blocks to precincts in demographic data

import pandas as pd
import os

#load csv
demo_data = pd.read_csv("../raw_data/Arizona/Apache.csv")
#make GEO.id match geojson format
demo_data["Id"] = demo_data["Id"].map(lambda x: x.lstrip('1000000US'))

block_id = censusblock['properties']['BLOCKID10']
precinct = feture['properties']['precinctna']
demo_index = demo_data.index[df['Id'] == block_id][0]
demo_data.at[demo_index, 'Precinct'] = 