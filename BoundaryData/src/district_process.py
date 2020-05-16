#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd

rows = []
state_properties = [("AZ", 'CD116FP'), ("OH", 'ID'), ("WI", 'District_N')]
with open("C:/Users/mlo10/IdeaProjects/GerryMander/assets/assets/congressional_districts.json") as f:
    districts = json.load(f)
    for state, property_num in state_properties:
        print(state)
        print(property_num)
        for district in districts[state]['features']:
            num = district['properties'][property_num]
            if(state == "AZ"):
                num = num.strip('0')
            del district["properties"]
            rows.append({
                "STATE": state,
                "DISTRICT": int(num),
                "BDY": json.dumps(district["geometry"])
            })
        
df_c = pd.DataFrame()
df_c = df_c.append(rows, ignore_index=True)


# In[2]:


print(df_c)


# In[3]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/CongDistrcts2.csv'
df_c.to_csv(path_or_buf=csv_file, index=False)


# In[ ]:




