#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# find duplicate UID values in all states

import pandas as pd

df_dup_total = pd.DataFrame()

def to_geojson(gap, num):
    return '{"type": "Feature", "geometry": '+ gap+', "properties":{"ID": '+str(num)+'}},'

def duplicates(state):
        file = state+'/precincts.csv'
        df = pd.read_csv(file, usecols=["UID", "BDY"])
        print(state)
        print(len(df.UID.unique()))
        df_dup = df[df.duplicated(['UID'])]
        df_dup_total = df_dup_total.append(df_dup)

duplicates("AZ")
duplicates("WI")
duplicates("OH")

file = 'duplicateUID.csv'
df_dup_total.to_csv(file)

file = open("duplicate.json", "w")
for precinct in df_dup_total.index:
    value = poo.at[precinct, "BDY"]
    bdy = to_geojson(value, precinct)
    file.write(bdy)
file.close()

print(df_dup_total)

