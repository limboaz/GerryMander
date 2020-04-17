import pandas as pd
county = "Yavapai"

def clean(file, year):
    df_AZ = pd.read_csv(file, encoding="latin-1", usecols=["PrecinctName", "ContestTitle", "Candidate Name",
                                                                     "Party Name", "Votes"], keep_default_na=False)
    # filter to just PRES and CON
    df_AZ = df_AZ[
        df_AZ['ContestTitle'].str.contains('PRESIDENTIAL') | df_AZ['ContestTitle'].str.contains(
            'SENATOR') | df_AZ['ContestTitle'].str.contains('REP')]
    # remove rows not needed
    df_AZ = df_AZ[~(df_AZ['Candidate Name'].str.contains("TotalVotes") | df_AZ['Candidate Name'].str.contains("Undervote") |
                       df_AZ['Candidate Name'].str.contains("Overvote"))]
    # trim precinct name to remove precinct_num
    df_AZ["PrecinctName"] = df_AZ["PrecinctName"].apply(lambda x: x[6:])
    # set uid
    df_AZ["UID"] = ""
    for i in df_AZ.index:
        df_AZ.at[i,'UID'] = "AZ_" + str(county).upper() + "_" + df_AZ["PrecinctName"][i].replace(" ", "").upper()
    
    return df_AZ

def agg_votes(df, year):
    print(df)
    df_agg = pd.DataFrame()
    df["VoteTotal"] = 0
    #iterate through og df
    index = 0
    voteCount = 0
    rows = []
    for i in df.index:
        #next candidate in the precinct
        if index != 0 and index % 3 == 0:
            rows.append({
                "UID": df.at[i, "UID"],
                "State": "AZ",
                "County": county,
                "Precinct": df.at[i,"PrecinctName"],
                "Year": year,
                "Contest": df.at[i, "ContestTitle"],
                "Party": df.at[i, "Party Name"],
                "Candidate": df.at[i, "Candidate Name"],
                "VoteTotal": voteCount
            })

            voteCount = 0
        else:
            voteCount += int(df.at[i, "Votes"])
        index += 1
    # print(rows)
    df_agg = df_agg.append(rows, ignore_index=True)
    return df_agg
        
file = "C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/raw_data/Arizona/Yavapai/2016_pres_results_county.csv"
df_AZ1 = clean(file, 2016)
df_AZ1 = agg_votes(df_AZ1, 2016)
file = "C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/raw_data/Arizona/Yavapai/2018_con_results_county.csv"
df_AZ2 = clean(file, 2018)
df_AZ2 = agg_votes(df_AZ2, 2018)
#combine
df_AZ = df_AZ1.append(df_AZ2, sort=False)
df_AZ.to_csv(path_or_buf="C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/Arizona/election_data_OpenElect.csv", index=False)