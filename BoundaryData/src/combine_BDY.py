#!/usr/bin/env python
# coding: utf-8

# In[1]:


# combine bdy files

import pandas as pd

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_bdy.csv'
df_1 = pd.read_csv(file)
districts = [-1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
df_1 = df_1[df_1["District"].isin(districts)]
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_fixedDistricts.csv'
df_2 = pd.read_csv(file)

df_combined = df_1.append(df_2, sort=False)
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_bdy2.csv'
df_combined.to_csv(file, index = False)


# In[2]:


print(df_combined)


# In[1]:


# combine bdy files

import pandas as pd

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_bdy.csv'
df_1 = pd.read_csv(file)
districts = [-1,1,2,3,4,5,6,7,8,9]
df_1 = df_1[df_1["District"].isin(districts)]
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_fixedDistricts2.csv'
df_2 = pd.read_csv(file)

df_combined = df_1.append(df_2, sort=False)
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_bdy2.csv'
df_combined.to_csv(file, index = False)

print(df_combined)


# In[ ]:


# combine bdy files

import pandas as pd

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ2.csv'
df_1 = pd.read_csv(file)
districts = [1,2,3,4,5,6,7,8,9]
df_1 = df_1[df_1["District"].isin(districts)]
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_fixedDistricts2.csv'
df_2 = pd.read_csv(file)

df_combined = df_1.append(df_2, sort=False)
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_bdy2.csv'
df_combined.to_csv(file, index = False)

