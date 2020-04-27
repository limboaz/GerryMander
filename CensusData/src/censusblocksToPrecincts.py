from shapely.geometry import shape
from shapely.strtree import STRtree
import json
import pandas as pd

# load blocks
csv_file = '../AZ_blocks.csv'
df_blocks = pd.read_csv(csv_file)
print(df_blocks)

blocks_bdy = []
for block in df_blocks.index:
    bdy = df_blocks.at[block, "BDY"]
    blocks_bdy.append(shape(json.loads(bdy)["geometry"]))
block_tree = STRtree(blocks_bdy)
index_by_id = dict((id(poly), i) for i, poly in enumerate(blocks_bdy))

# load precinct df
csv_file = '../../BoundaryData/BOUNDARY_DATA/AZ_bdy.csv'
df_pop = pd.read_csv(csv_file, usecols=["UID", "BDY"])

# set up df for precinct uid, population data
block_cols = list(df_blocks.columns)[2:]
for col in block_cols:
    df_pop[col] = 0
    
# If a census block spans multiple precincts, census content can be assigned to the precincts based on a percentage of area
# keep block_ids that were matched
matched_blocks = []
# assign a precinct to census block data
for precinct in df_pop.index:
    precinct_bdy = df_pop.at[precinct, "BDY"].replace("\'", "\"")
    precinct_bdy = shape(json.loads(precinct_bdy)["geometry"])
    closest = [(index_by_id[id(poly)], poly) for poly in block_tree.query(precinct_bdy)]
    # blocks_precinct = []
    # iterate through the query result to find blocks contained within precinct
    for block_id,block in closest:
        if precinct_bdy.contains(block):
            # set pop data in precinct
            for col in block_cols:
                cur_value = df_pop.at[precinct, col]
                df_pop.at[precinct, col] = cur_value + df_blocks.at[block_id, col]
                matched_blocks.append(df_blocks.at[block_id, "Id"])

# check if all precincts were matched
print("PRECINCTS WITH NO MATCH: "+str(len(df_pop[df_pop["Total:"] == 0])))
# check if all blocks were matched
print("BLOCKS WITH NO MATCH: "+str(len(df_blocks[~df_blocks["Id"].isin(matched_blocks)])))

# drop bdy field in df_pop
df_pop = df_pop.drop(columns = "BDY").rename(columns = {"Total:" : "Total"})
print(df_pop)
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/preprocess/AZ_pop.csv'
df_pop.to_csv(csv_file, index=False)