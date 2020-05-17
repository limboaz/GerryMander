import pandas as pd

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ_fixed.csv'
df = pd.read_csv(file)
cochise_map = []
with open('C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_cochise_ED_mapping.txt') as f:
     cochise_map = f.readlines()
cochise_map = list(map(lambda precinct: precinct.strip('\n'), cochise_map))
        
print(cochise_map)
print(len(cochise_map))

df_cochise = df[df["County"] == "Cochise"]
uids = df_cochise.UID.unique()
print(len(uids))
print(uids)

for precinct in df_cochise.index:
    ed_name = df.at[precinct, "UID"][len("AZ_COCHISE_"):]
    cochise_num = cochise_map.index(ed_name)+1
    if cochise_num < 10:
        cochise_num = "0"+str(cochise_num)
    print(ed_name)
    curPrecinct = "PRECINCT"+str(cochise_num)
    curPrecinct = "AZ_COCHISE_" + curPrecinct
    df.at[precinct, "UID"] = curPrecinct
    
print(df[df["County"] == "Cochise"])
    

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ_fixed2.csv'
df.to_csv(file, index=False)

error_types = [
    "UNASSIGNED_AREA",
    "OVERLAPPING",
    "SELF_INTERSECTING",
    "ENCLOSED_PRECINCT",
    "MULTIPOLYGON",
    "ZERO_POPULATION",
    "ZERO_ELECTION_DATA",
    "VOTE_NOT_PROPORTIONAL_TO_POP"
]

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_bdy2.csv'
df_bdy2 = pd.read_csv(file, usecols=["UID"])

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ_fixed2.csv'
# df_ed = pd.read_csv(file, usecols=["UID", "State", "County", "Precinct"])
ed = pd.read_csv(file, usecols=["UID", "Year"])
ed_16 = ed[ed["Year"] == 2016].UID.unique()
ed_18 = ed[ed["Year"] == 2018].UID.unique()

print(len(ed_16))
print(len(ed_18))

df_data_errors = pd.DataFrame()
data_errors = []

#find election data errors
df_zero_elec = df_bdy2[~df_bdy2["UID"].isin(ed_16) | ~df_bdy2["UID"].isin(ed_18)]
#create errors
for precinct in df_zero_elec.index:
    data_errors.append({
        "Type": error_types[6],
        "Datasource": "azsos.gov",
        "PrecinctsAssociated": df_zero_elec.at[precinct, "UID"],
        "ErrorValue": 0.0
    })
    
df_data_errors = df_data_errors.append(data_errors, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_data_errors2.csv'
df_data_errors.to_csv(path_or_buf=csv_file, index=False)

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ_fixed2.csv'
ed = pd.read_csv(file)
df_bdy2 = df_bdy2.UID.unique()
df_elec = ed[ed["UID"].isin(df_bdy2)]
# df_matched = df_ed[df_ed["UID"].isin(df_elec)]
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_matched_ed.csv'
df_elec.to_csv(path_or_buf=csv_file, index=False)


# WI
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_bdy2.csv'
df_bdy2 = pd.read_csv(file, usecols=["UID"]).UID.tolist()

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_WI_fixed2.csv'
df = pd.read_csv(file)
df_1_ward = df[df["UID"].str.contains('WARD[\d]+', regex=True)]
print(df_1_ward)

print(df_bdy2)

import re
expr = r"_[A-Z\.\-]+WARD"
matches = 0
for row in df_1_ward.index:
    ed_UID = df.at[row, "UID"]
#     print(ed_UID)
    beg = ed_UID.index(re.search(expr, ed_UID).group(0))
    ed_precinct = ed_UID[beg:ed_UID.index("WARD")]
#     print(ed_precinct)
    matching = list(filter(lambda element: ed_precinct in element, df_bdy2))
    if(len(matching) == 1):
#         print(matching)
        df.at[row, "UID"] = matching[0]
        matches = matches + 0

print(matches)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_WI_fixed3.csv'
df.to_csv(path_or_buf=csv_file, index=False)

error_types = [
    "UNASSIGNED_AREA",
    "OVERLAPPING",
    "SELF_INTERSECTING",
    "ENCLOSED_PRECINCT",
    "MULTIPOLYGON",
    "ZERO_POPULATION",
    "ZERO_ELECTION_DATA",
    "VOTE_NOT_PROPORTIONAL_TO_POP"
]

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_bdy2.csv'
df_bdy2 = pd.read_csv(file, usecols=["UID"])

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_WI_fixed3.csv'
# df_ed = pd.read_csv(file, usecols=["UID", "State", "County", "Precinct"])
ed = pd.read_csv(file)
ed_UID = ed.UID.unique()
ed_16 = ed[ed["Year"] == 2016].UID.unique()
ed_18 = ed[ed["Year"] == 2018].UID.unique()

df_data_errors = pd.DataFrame()
data_errors = []

#find election data errors
df_zero_elec = df_bdy2[~(df_bdy2["UID"].isin(ed_16) & df_bdy2["UID"].isin(ed_18))]
#create errors
for precinct in df_zero_elec.index:
    data_errors.append({
        "Type": error_types[6],
        "Datasource": "electionlab.mit.edu",
        "PrecinctsAssociated": df_zero_elec.at[precinct, "UID"],
        "ErrorValue": 0.0
    })
    
df_data_errors = df_data_errors.append(data_errors, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_data_errors3.csv'
df_data_errors.to_csv(path_or_buf=csv_file, index=False)

df_bdy2 = df_bdy2.UID.unique()
df_elec = ed[ed["UID"].isin(df_bdy2)]
# df_matched = df_ed[df_ed["UID"].isin(df_elec)]
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/WI_matched_ed.csv'
df_elec.to_csv(path_or_buf=csv_file, index=False)

# OH
error_types = [
    "UNASSIGNED_AREA",
    "OVERLAPPING",
    "SELF_INTERSECTING",
    "ENCLOSED_PRECINCT",
    "MULTIPOLYGON",
    "ZERO_POPULATION",
    "ZERO_ELECTION_DATA",
    "VOTE_NOT_PROPORTIONAL_TO_POP"
]

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_bdy2.csv'
df_bdy2 = pd.read_csv(file, usecols=["UID"]).UID

# file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_OH-Copy.csv'
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_matched_ed.csv'
# df_ed = pd.read_csv(file, usecols=["UID", "State", "County", "Precinct"])
df_ed = pd.read_csv(file, usecols=["UID", "Year"])
ed_16 = df_ed[df_ed["Year"] == 2016].UID.unique()
ed_18 = df_ed[df_ed["Year"] == 2018].UID.unique()
print(len(ed_16))
print(len(ed_18))
oops = [s for s in ed_16 if not s in ed_18]
print(len(oops))
df_zero_bdy = df_ed.UID.unique()
print(len(df_zero_bdy))

df_data_errors = pd.DataFrame()
data_errors = []
df_ed = pd.read_csv(file)
# ed_16 = df_ed[df_ed["Year"] == 2016].UID.unique()
# ed_18 = df_ed[df_ed["Year"] == 2018].UID.unique()
#find election data errors
df_elec = df_ed[df_ed["UID"].isin(df_bdy2)]
# df_matched = df_ed[df_ed["UID"].isin(df_elec)]
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_matched_ed2.csv'
df_elec.to_csv(path_or_buf=csv_file, index=False)
# #create errors
# for precinct in df_zero_elec.index:
#     data_errors.append({
#         "Type": error_types[6],
#         "Datasource": "sos.state.oh.us",
#         "PrecinctsAssociated": df_zero_elec.at[precinct, "UID"],
#         "ErrorValue": 0.0
#     })

    
# df_data_errors = df_data_errors.append(data_errors, ignore_index=True)

# csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_data_errors2.csv'
# df_data_errors.to_csv(path_or_buf=csv_file, index=False)

