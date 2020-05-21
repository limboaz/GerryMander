#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd

file = 'WI/precincts.csv'
df = pd.read_csv(file, usecols=["District", "BDY"])


# In[16]:


df_d = df[df["District"] < 0]
print(df_d)


# In[4]:


from shapely.geometry import shape
from shapely.ops import unary_union
import json

bdy = []

for i in df_d.index:
    bdy.append(shape(json.loads(df_d.at[i, "BDY"])))
    
district = unary_union(bdy)
print(district)


# In[5]:


def to_geojson(gap):
    return '{"type": "Feature", "geometry": {"type": "'+str(gap.geom_type)+'", "coordinates": ['+str(list(gap.exterior.coords))+']}},'


# In[7]:


row = {
    "STATE": "WI",
    "DISTRICT": -1.0,
    "BDY": json.dumps(shapely.geometry.mapping(district))
}


# In[12]:


file = 'district.csv'
file = open(file, 'w')
file.write(str(row))
file.close()

