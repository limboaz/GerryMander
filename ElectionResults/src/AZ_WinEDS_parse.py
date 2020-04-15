import pandas as pd

party = ["NA","REP", "DEM", "LBT", "GRN", "IND", ""]

#create csv file for WinEDS type formatting
def clean(file, year, county):
    #read dataframe for needed col
    df_AZ = pd.read_csv(file, sep="\t", encoding="latin-1", usecol=["PRECINCT_NAME", "CONTEST_FULL_NAME", "CANDIDATE_FULL_NAME", "TOTAL"])
    #TODO: only keep pres and con rows
    #TODO: get appropriate party name from candidate_party_id mapping
    df_AZ[candidate_party_id] = df_AZ[candidate_party_id].map(lambda x: x = party[x])
    #set year
    df_AZ["Year"] = year
    #set county
    df_AZ["County"] = county
    #return dataframe
    return df_AZ

#MARICOPA
df_AZ = pd.read_csv("../raw_data/Arizona/Maricopa/2016_pres_results_county.txt", sep="\t", encoding="latin-1", col)
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

