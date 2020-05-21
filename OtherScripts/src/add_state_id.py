#!/usr/bin/env python
# coding: utf-8

# In[1]:


# add state to errors (needed to add state id after already creating csv so just wrote this simple script)
import pandas as pd
file = 'AZ/errors.csv'
df = pd.read_csv(file)
df["StateId"] = "AZ"

df.to_csv(file, index=False)


# In[2]:


file = 'WI/errors.csv'
df = pd.read_csv(file)
df["StateId"] = "WI"

df.to_csv(file, index=False)


# In[6]:


import pandas as pd
file = r"C:\Users\mlo10\Downloads\errorsOH (1).csv"
df = pd.read_csv(file)
df["StateId"] = "OH"
df.to_csv(file, index=False)


# In[ ]:




