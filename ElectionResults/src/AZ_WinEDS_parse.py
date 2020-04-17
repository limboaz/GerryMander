import pandas as pd

party = ["NA", "REP", "DEM", "LBT", "GRN", "IND", ""]

#create csv file for WinEDS type formatting
def cleanWinEDS(file, year, county):
    #read dataframe for needed col
    df_AZ = pd.read_csv(file, sep="\t", encoding="latin-1", usecols=["PRECINCT_NAME", "CONTEST_FULL_NAME", "candidate_party_id", "CANDIDATE_FULL_NAME", "TOTAL"])
    #filter to just PRES and CON
    df_AZ = df_AZ[df_AZ['CONTEST_FULL_NAME'].str.contains('Presidential Electors') | df_AZ['CONTEST_FULL_NAME'].str.contains('US Senate') | df_AZ['CONTEST_FULL_NAME'].str.contains('Rep')]
    #map party_id to party
    df_AZ["candidate_party_id"] = df_AZ["candidate_party_id"].apply(lambda x: party[int(x)])
    #trim precinct name to remove precinct_num
    df_AZ["PRECINCT_NAME"] = df_AZ["PRECINCT_NAME"].apply(lambda x: x[5:])
    #set uid
    df_AZ["UID"] = ""
    for i in df_AZ.index:
        df_AZ["UID"][i] = "AZ_"+str(county).upper()+"_"+df_AZ["PRECINCT_NAME"][i].replace(" ", "").upper()
    #set year
    df_AZ["Year"] = year
    #set county
    df_AZ["County"] = county
    df_AZ["State"] = "AZ"
    #return dataframe
    return df_AZ


#MARICOPA
file = "../raw_data/Arizona/Maricopa/2016_pres_results_county.txt"
df_AZ1 = cleanWinEDS(file, 2016, "Maricopa")
file = "../raw_data/Arizona/Maricopa/2018_con_results_county.txt"
df_AZ2 = cleanWinEDS(file, 2018, "Maricopa")
#combine
df_AZ1 = df_AZ1.append(df_AZ2, sort=False)
# reorder col
cols = list(df_AZ1.columns.values)
cols_reordered = [cols[5], cols[8], cols[7], cols[0], cols[6], cols[3], cols[2], cols[1], cols[4]]
df_AZ1 = df_AZ1[cols_reordered]
#save data to csv
df_AZ1.to_csv(path_or_buf="../preprocess/Arizona/election_data_WinEDS.csv", index=False)

