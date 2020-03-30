import pandas as pd

#extract boundaries for values in ElectionWare file
def county_key_value(county_key, col):
    row = county_key[county_key.FIELD_TYPE == col].index[0]
    indices = [county_key.at[row, "START_POSITION"]-1, county_key.at[row, "END_POSITION"]]
    return indices

#list of counties that use ElectionWare
counties_ew_16 = ["Apache", "Cochise", "Gila", "Graham", "Greenlee", "Mohave", "Navajo", "Pima", "Pinal", "Santa_Cruz"]
counties_ew_18 = ["Apache", "Cochise", "Gila", "Graham", "Greenlee", "Mohave", "Navajo", "Pima", "Pinal", "Santa_Cruz", "La_Paz", "Yuma"]
counties_ew = [counties_ew_16, counties_ew_18]
years = ["2016_pres", "2018_con"]
#create csv for ew counties
#store other votes like Late Early Votes in col = 'OtherVotes'
rows = []
#iterate through each election year
index = 0
for year in years:
    #load key for cleaning data
    file = "../raw_data/Arizona/EW_"+str(year[0:4])+".csv"
    key_EW = pd.read_csv(file)
    #iterate through each county
    for county in counties_ew[index]:
        #filter key to just the current county
        county_key = key_EW[key_EW.COUNTY == county]
        #open election results for that county
        file = open('../raw_data/Arizona/'+str(county)+'/'+str(year)+'_results_county.txt', 'r')
        #create election result dataframe
        df_AZ = pd.DataFrame(columns = ["UID", "State", "County", "Precinct", "Year", "Contest", "Party", "Candidate", "VoteTotal"])
        #set indices accordingly
        precinct_name_indices = county_key_value(county_key, "Precinct Name")
        subJur_start_index = 234
        #parse ElectionWare nonsense formatting
        data = file.readlines()
        #rows = []
        for i in data:
            rows.append({
                "UID": str("AZ_"+county+"_"+i[precinct_name_indices[0]:precinct_name_indices[1]].strip()).upper(),
                "State": "AZ",
                "County": county,
                "Precinct": i[precinct_name_indices[0]:precinct_name_indices[1]].strip(),
                "Year": str(year[0:4]),
                "Contest": i[111:167].strip().upper(),
                "Party": i[101:104].strip(),
                "Candidate": i[167:205].strip(),
                "VoteTotal": int(i[11:17])
            })
    index += 1
    file.close()
df_AZ = df_AZ.append(rows, sort=False)
#filter out non presidential or US House data
df_AZ = df_AZ[df_AZ['Contest'].str.contains('PRESIDENTIAL ELECTORS') | df_AZ['Contest'].str.contains('REP')]
csv_file = '../preprocess/Arizona/election_data_EW2.csv'
df_AZ.to_csv(path_or_buf=csv_file, index=False)
