#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
# combine error files
state_po = "AZ"
#bdy data
file = str(state_po)+'/precincts.csv'
df_bdy = pd.read_csv(file, usecols=["UID", "BDY"])

# zero elections
file = str(state_po)+'/ZERO_ELECTION_ERROR_CLEANED.csv'
df_ze = pd.read_csv(file, usecols=["Type","Datasource","PrecinctsAssociated"])
df_ze["GeoJSON"] = ""
for error in df_ze.index:
    error_UID = df_ze.at[error, "PrecinctsAssociated"]
    bdy = df_bdy.loc[df_bdy["UID"] == error_UID]["BDY"].tolist()[0]
    df_ze.at[error, "GeoJSON"] = bdy


# In[93]:


print(df_ze)
print(df_ze[df_ze["GeoJSON"].isnull()])


# In[94]:


# proportion error
file = str(state_po)+'/PROPORTION_ERROR.csv'
df_p = pd.read_csv(file, usecols=["Type","Datasource","PrecinctsAssociated"])
df_p["GeoJSON"] = ""
for error in df_p.index:
    error_UID = df_p.at[error, "PrecinctsAssociated"]
    bdy = df_bdy.loc[df_bdy["UID"] == error_UID]["BDY"].tolist()[0]
    df_p.at[error, "GeoJSON"] = bdy
print(df_p)
print(df_p[df_p["GeoJSON"].isnull()])


# In[95]:


# population error
file = str(state_po)+'/ZERO_POPULATION_ERROR.csv'
df_pop = pd.read_csv(file)
print(df_pop)
print(df_pop[df_pop["GeoJSON"].isnull()])
# bdy error
file = str(state_po)+'/BDY_ERROR.csv'
df_bdy_error = pd.read_csv(file)
print(df_bdy_error)
print(df_bdy_error[df_bdy_error["GeoJSON"].isnull()])


# In[96]:


# combine all the dataframes
df = df_ze.append(df_p, ignore_index=True)
df = df.append(df_pop, ignore_index=True)
df = df.append(df_bdy_error, ignore_index=True)
df["districtAssociated"] = ""
print(df)


# In[74]:


def to_geojson(gap, num):
    return '{"type": "Feature", "geometry": '+ gap+', "properties":{"ID": '+str(num)+'}},'


# In[86]:


# get unassinged area districts
df_unassigned = df[df["Type"] == "UNASSIGNED_AREA"]

file = open("WI_unassigned.json", "w")
for precinct in df_unassigned.index:
    value = df_unassigned.at[precinct, "GeoJSON"]
    bdy = to_geojson(value, precinct)
    file.write(bdy)
file.close()


# In[87]:


print(df_unassigned)


# In[88]:


# manually assign the district to the unassigned area (could easily be done with the get_district function in the precinct_process script)
# this one was for WI

df.at[6388, "districtAssociated"] = -1
df.at[6148, "districtAssociated"] = -1
df.at[6478, "districtAssociated"] = -1
df.at[6313, "districtAssociated"] = -1


# In[90]:


print(df[df["districtAssociated"].isin([-1])])


# In[97]:


file = str(state_po)+"/errors.csv"
df.to_csv(file, index=False)


# In[ ]:




