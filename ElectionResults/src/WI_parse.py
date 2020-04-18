import pandas as pd

def clean2016(file, typeElect):
    WI_df = pd.read_csv(file, encoding="latin-1", low_memory=False, usecols=['state_postal', 'county_name', 'precinct', 'office', 'party', 'candidate', 'votes'], keep_default_na=False)
    
    contest = ""
    if typeElect == "CON":
        contest = 'US House'
    else:
        contest = 'US President'
    
    WI_df = WI_df[WI_df.state_postal == 'WI']
    WI_df = WI_df[WI_df.office == contest]

    p = ["democratic", "republican", "libertarian", "green", "independent"]
    WI_df = WI_df[WI_df["party"].isin(p)]

    party_key = {"democratic": "DEM", "republican": "REP", "libertarian": "LIB", "green": "GRN", "independent": "IND"}
    WI_df["UID"] = ""
    WI_df["office"] = typeElect
    WI_df["year"] = 2016

    # iterate through rows
    for i in WI_df.index:
        WI_df.at[i, "UID"] = "WI_" + WI_df.at[i, 'county_name'].upper() + "_" + WI_df.at[i, "precinct"].replace(" ", "").upper()
        WI_df.at[i, "party"] = party_key[WI_df.at[i, "party"]]
    
    return WI_df

#get 2016_con
file = r"C:\Users\mlo10\IdeaProjects\GerryMander\ElectionResults\raw_data\Wisconsin\2016-precinct-house.csv"
df_c16 = clean2016(file, "CON")

#get 2016_pres
file = r"C:\Users\mlo10\IdeaProjects\GerryMander\ElectionResults\raw_data\Wisconsin\2016-precinct-president.csv"
df_p16 = clean2016(file, "PRES")

# combine
df_c16 = df_c16.append(df_p16, sort=False)

#get 2018_con
file = "../raw_data/Wisconsin/precinct_2018.csv"
WI_df = pd.read_csv(file, encoding="latin-1", low_memory=False, usecols=['state_po', 'county', 'precinct', 'office', 'party', 'candidate', 'votes'], keep_default_na=False)

typeElect = "CON"

WI_df = WI_df[WI_df.state_po == 'WI']
WI_df = WI_df[WI_df.office == 'US House']

p = ["democratic", "republican", "libertarian", "green", "independent"]
WI_df = WI_df[WI_df["party"].isin(p)]

party_key = {"democratic": "DEM", "republican": "REP", "libertarian": "LIB", "green": "GRN", "independent": "IND"}
WI_df["UID"] = ""
WI_df["office"] = typeElect
WI_df["year"] = 2018

# iterate through rows
for i in WI_df.index:
    WI_df.at[i, "UID"] = "WI_" + WI_df.at[i, 'county'].upper() + "_" + WI_df.at[i, "precinct"].replace(" ", "").upper()
    WI_df.at[i, "party"] = party_key[WI_df.at[i, "party"]]
    
# rename cols
WI_df = WI_df.rename(columns={"state_po": "state_postal", "county": "county_name"})

# combine
df_c16 = df_c16.append(WI_df, sort=False)

# rename cols
df_c16 = df_c16.rename(columns={"state_postal": "State", "county_name": "County", "precinct": "Precinct",
 "candidate": "Candidate", "office": "Contest", "party": "Party", "votes": "VoteTotal", "year": "Year"})
# reorder cols
df_c16 = df_c16.reindex(columns=["UID", "State", "County", "Precinct", "Year", "Contest", "Party", "Candidate", "VoteTotal"])

df_c16.to_csv(path_or_buf=r'C:\Users\mlo10\IdeaProjects\GerryMander\ElectionResults\preprocess\Wisconsin\election_data.csv', index=False)
