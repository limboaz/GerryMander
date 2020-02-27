import pandas as pd

#MARICOPA
#create csv file for WinEDS type formatting
df_AZ = pd.read_csv("../raw_data/Arizona/Maricopa/2016_pres_results_county.txt", sep="\t", encoding="latin-1")
df_AZ["Year"] = 2016
df_AZ["County"] = "Maricopa"

df_AZ2 = pd.read_csv("../raw_data/Arizona/Maricopa/2018_con_results_county.txt", sep="\t", encoding="latin-1")
df_AZ2["Year"] = 2018
df_AZ2["County"] = "Maricopa"

#combine
df_AZ = df_AZ.append(df_AZ2, sort=False)
df_AZ.to_csv(path_or_buf="../preprocess/Arizona/election_data_WinEDS.csv", index=False)

#YAVAPAI
#create csv file for OpenElect type formatting
df_AZ = pd.read_csv("../raw_data/Arizona/Yavapai/2016_pres_results_county.txt", sep="\t", encoding="latin-1")
df_AZ["Year"] = 2016
df_AZ["County"] = "Yavapai"

df_AZ2 = pd.read_csv("../raw_data/Arizona/Yavapai/2018_con_results_county.txt", sep="\t", encoding="latin-1")
df_AZ2["Year"] = 2018
df_AZ2["County"] = "Yavapai"

#combine
df_AZ = df_AZ.append(df_AZ2, sort=False)
df_AZ.to_csv(path_or_buf="../preprocess/Arizona/election_data_OpenElect.csv", index=False)

