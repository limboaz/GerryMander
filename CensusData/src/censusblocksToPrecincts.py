# If a census block spans multiple precincts, census content can be assigned to the precincts based on a percentage of area
# assign a precinct to census block data
# object.intersect(other)
# object.within(other)

from shapely.geometry import shape
from shapely.strtree import STRtree
import json, pickle
import pandas as pd

#load census block geojson
with open("../raw_data/Geography/GeoJSON/censusblock_az.json") as f:
    blocks_gj = json.load(f)["features"]
#load precinct df
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ.csv'
df_p = pd.read_csv(csv_file, usecols=["UID", "BDY"])
precinct_poly = list(df_p["BDY"])
precinct_tree = STRtree(precinct_poly)
#assign a precinct to census block data
block_to_precinct_map = {}
for censusblock in blocks_gj:
    #find what precincts overlap the census blocks
    block = shape(precinct['geometry'])
    closest = precinct_tree.query(block)
    print(str(closest))
    # for poly in closest:
        # if block.within(poly):
            #get the block ID to add the precinct to the demographic data
            # block_id = censusblock['properties']['BLOCKID10']
            # poly_index = precinct_poly.index(poly) if poly in precinct_poly else -1
            # print("------------------NEW GUY----------")
            # print(poly_index)
            # print(precinct_poly[poly_index])
            # print(precinct_names[poly_index])
            #exit(0)
            # block_to_precinct_map[block_id] = precinct_names[poly_index]
            # print(str(block_to_precinct_map))
            #exit(0)

#TODO: load to pickle file to look at the file in
