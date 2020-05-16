#!/usr/bin/env python
# coding: utf-8

# In[2]:


from shapely.geometry import shape
from shapely.strtree import STRtree
import json, pickle
import pandas as pd


# In[3]:


# load blocks
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/OH_blocks.csv'
df_blocks = pd.read_csv(csv_file)
print(df_blocks)


# In[4]:


blocks_bdy = []
for block in df_blocks.index:
#     jsonify = block.replace("\'", "\"")
    bdy = df_blocks.at[block, "BDY"]
    blocks_bdy.append(shape(json.loads(bdy)))
block_tree = STRtree(blocks_bdy)
index_by_id = dict((id(poly), i) for i, poly in enumerate(blocks_bdy))


# In[5]:


# load precinct df
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_bdy2.csv'
df_pop = pd.read_csv(csv_file, usecols=["UID", "BDY"])


# In[6]:


# set up df for precinct uid, population data
block_cols = list(df_blocks.columns)[2:]
for col in block_cols:
    df_pop[col] = 0
print(df_pop)


# In[7]:


# If a census block spans multiple precincts, census content can be assigned to the precincts based on a percentage of area
# keep block_ids that were matched
matched_blocks = []
# assign a precinct to census block data
for precinct in df_pop.index:
    precinct_bdy = df_pop.at[precinct, "BDY"]
    precinct_bdy = shape(json.loads(precinct_bdy))
    precinct_area = precinct_bdy.area
    closest = [(index_by_id[id(poly)], poly) for poly in block_tree.query(precinct_bdy)]
    # iterate through the query result to find blocks contained within precinct
    for block_id,block in closest:
        # contained in precinct
        if precinct_bdy.contains(block):
             for col in block_cols:
                cur_value = df_pop.at[precinct, col]
                df_pop.at[precinct, col] = cur_value + df_blocks.at[block_id, col]
                matched_blocks.append(df_blocks.at[block_id, "Id"])
        # blocks that aren't completely contained in precinct
        elif precinct_bdy.intersects(block):
            # set pop data in precinct
            block_area = block.area
            intersection_area = block.intersection(precinct_bdy).area
            block_weight = intersection_area/block_area
            for col in block_cols:
                cur_value = df_pop.at[precinct, col]
                df_pop.at[precinct, col] = cur_value + df_blocks.at[block_id, col]*block_weight
                matched_blocks.append(df_blocks.at[block_id, "Id"])
print(df_pop)


# In[13]:


# check if all precincts were matched
df_unmatched_p = df_pop[df_pop["Total:"] == 0]
print(len(df_unmatched_p))


# In[9]:


zero_pop_error = []
df_error = pd.DataFrame()

for i in df_unmatched_p.index:
    zero_pop_error.append({
        "Type" : "ZERO_POPULATION",
        "Datasource" : "census.gov",
        "PrecinctsAssociated" : df_unmatched_p.at[i, "UID"],
        "GeoJSON" : df_unmatched_p.at[i, "BDY"]
    })
df_error = df_error.append(zero_pop_error, ignore_index=False)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/preprocess/OH_pop_error.csv'
df_error.to_csv(csv_file, index=False)


# In[10]:


# check if all blocks were matched
df_unmatched_b = df_blocks[~df_blocks["Id"].isin(matched_blocks)]
print(len(df_unmatched_b))


# In[11]:


# drop bdy field in df_pop
df_pop = df_pop.drop(columns = "BDY").rename(columns = {"Total:" : "Total"})
print(df_pop)


# In[12]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/preprocess/OH_pop.csv'
df_pop.to_csv(csv_file, index=False)


# In[12]:


file = open('C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/blocks_WI.pkl' , 'wb')
pickle.dump(block_tree, file)
file.close()


# In[13]:


file = open('C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/blocks_by_id_WI.pkl' , 'wb')
pickle.dump(index_by_id, file)
file.close()


# In[18]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/preprocess/AZ_pop_unmatched_p.csv'
df_unmatched_p.to_csv(csv_file, index=False)
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/preprocess/AZ_pop_unmatched_b.csv'
df_unmatched_b.to_csv(csv_file, index=False)