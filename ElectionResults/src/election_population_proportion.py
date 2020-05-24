#!/usr/bin/env python
# coding: utf-8

# In[45]:


# aggregate popoulation by election per precinct and compare it to that precincts population.
# If less than X% of the population voted, then flag as error
# OR if there are more votes than populatoin

import pandas as pd

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_matched_ed.csv'
df_ed = pd.read_csv(file)
df_ed = df_ed[df_ed["Year"] == 2016]
df_ed = df_ed[df_ed["Contest"] == "PRES"]
file = csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/CensusData/preprocess/WI_pop.csv'
df_pop = pd.read_csv(file, usecols=["UID", "Total"])

df_ed_agg = pd.DataFrame()
ed_agg = []
for UID in df_ed.UID.unique():
    total_votes = 0
    for i in df_ed[df_ed["UID"] == UID].index:
        total_votes = total_votes + df_ed.at[i, "VoteTotal"]
    ed_agg.append({"UID": UID, "Total": total_votes})  
df_ed_agg = df_ed_agg.append(ed_agg, sort=False)
print(df_ed_agg)


# In[46]:


errors = []
count = 0
count2 = 0
for precinct in df_ed_agg.index:
    ed_UID = df_ed_agg.at[precinct, "UID"]
    ed_total = df_ed_agg.at[precinct, "Total"]
    population = df_pop.loc[df_pop["UID"] == ed_UID]["Total"].tolist()[0]
    if population < ed_total:
        count2 = count2 + 1
        errors.append({
            "Type" : "MORE_VOTES_THAN_POP",
            "Datasource" : "census.gov",
            "PrecinctsAssociated" : ed_UID,
            "ErrorValue": ed_total
        })
    elif ed_total/population < 0.30:
        count = count + 1
        errors.append({
            "Type" : "VOTE_NOT_PROPORTIONAL_TO_POP",
            "Datasource" : "census.gov",
            "PrecinctsAssociated" : ed_UID,
            "ErrorValue": round(ed_total/population*100, 2)
        })
print(len(errors))
print(count)
print(count2)


# In[47]:


df = pd.DataFrame(errors)
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_proportion_error.csv'
df.to_csv(file, index=False)


# In[48]:


file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_election_totals.csv'
df_ed_agg.to_csv(file, index=False)


# In[ ]:




