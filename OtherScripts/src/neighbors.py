#!/usr/bin/env python
# coding: utf-8

# In[13]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Neighbors
from shapely.geometry import shape
from shapely.strtree import STRtree
from shapely.ops import unary_union
import json, pickle, csv
import pandas as pd
import math

def distance(point1, point2):
    return math.acos(math.sin(math.radians(point1[1]))*math.sin(math.radians(point2[1]))
                     +math.cos(math.radians(point2[1]))*math.cos(math.radians(point1[1]))
                     *math.cos(math.radians(point2[0])-math.radians(point1[0])))*20902230

# change starting index for each state so no overlaps
generateId = 300000

    
df_neighbors = []
file = 'precincts_OH (1).csv'
df = pd.read_csv(file)

precincts_bdy = []
for i in df.index:
    poly = shape(json.loads(df.at[i, "BDY"]))
    precincts_bdy.append(poly)

precinct_tree = STRtree(precincts_bdy)
index_by_id = dict((id(poly), i) for i, poly in enumerate(precincts_bdy))

for precinct_id, precinct_bdy in enumerate(precincts_bdy):
    closest = [(index_by_id[id(poly)], poly) for poly in precinct_tree.query(precinct_bdy)]
    for neighbor_id, neighbor_bdy in closest:
        if neighbor_bdy.intersects(precinct_bdy) and not neighbor_bdy.equals(precinct_bdy):
            intersection = neighbor_bdy.intersection(precinct_bdy)
            if intersection.type == 'LineString':
                if distance(intersection.coords[0], intersection.coords[1]) >= 500.0:
                    df_neighbors.append({
                        "id": str(generateId),
                        "neighborid": df.at[neighbor_id,"UID"],
                        "precinct_uid": df.at[precinct_id, "UID"]
                    })
                    generateId+=1
            elif intersection.type == 'MultiLineString':
                for i in intersection:
                    if distance(i.coords[0], i.coords[1]) >= 200.0:
                        df_neighbors.append({
                            "id": str(generateId),
                            "neighborid": df.at[neighbor_id,"UID"],
                            "precinct_uid": df.at[precinct_id, "UID"]
                        })
                        break
                        generateId+=1

neighbors = pd.DataFrame(df_neighbors)
file = 'neighbors_OH.csv'
neighbors.to_csv(file, index=False)  


# In[14]:


print(neighbors)


# In[ ]:




