import pandas as pd

def clean(file, year, type_elect, senate_bdy):
    df_OH = pd.read_csv(file, encoding="latin-1")
    cols = list(df_OH.columns.values)
    df = pd.DataFrame()
    party_key = {"(D)": "DEM", "(R)": "REP", "(G)": "GRN", "(WI)*": "WI", "(L)": "LIB"}
    remove_wi = "WI" if type_elect is "CON" else ""
    rows = []
    
    # iterate though precincts
    for i in df_OH.index:
        # iterate through candidates
        # index in cols where candidates start: senate_bdy
        for can_i in range(senate_bdy,len(cols)):
            candidate = cols[can_i]
            if "(" in candidate:
                bdy = candidate.index("(")
                party = party_key[candidate[bdy:]]
                candidate = candidate[:bdy-1]
            else: 
                party = "IND"
            voteTotal = int(df_OH.at[i, cols[can_i]].replace(",", "")) if type(df_OH.at[i, cols[can_i]]) is str else df_OH.at[i, cols[can_i]]
            
            if voteTotal > 0 and party is not remove_wi:
                rows.append({
                    "UID": "OH_" + df_OH.at[i, 'County Name'].upper() + "_" + df_OH.at[i, "Precinct Name"].replace(" ", "").upper(),
                    "State": "OH",
                    "County": df_OH.at[i, 'County Name'],
                    "Precinct": df_OH.at[i, "Precinct Name"],
                    "Year": year,
                    "Contest": "PRES" if type_elect is "PRES" else "CON",
                    "Party": party,
                    "Candidate": candidate,
                    "VoteTotal": voteTotal
                })

    return df.append(rows, ignore_index=True)


file = r"C:\Users\mlo10\IdeaProjects\GerryMander\ElectionResults\raw_data\Ohio\2016_pres_results_precinct.csv"
dfP2016 = clean(file, 2016, "PRES", 8)

file = r"C:\Users\mlo10\IdeaProjects\GerryMander\ElectionResults\raw_data\Ohio\2016_con_results_precinct.csv"
dfC2016 = clean(file, 2016, "CON", 15)

df = dfP2016.append(dfC2016, sort=False)

file = r"C:\Users\mlo10\IdeaProjects\GerryMander\ElectionResults\raw_data\Ohio\2018_con_results_precinct.csv"
dfC2018 = clean(file, 2018, "CON", 11)

df = df.append(dfC2018, sort=False)
df.to_csv(path_or_buf=r"C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/Ohio/election_data2.csv", index=False)