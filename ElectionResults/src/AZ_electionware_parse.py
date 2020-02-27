import pandas as pd
#import os

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
    #iterate through each county
    for county in counties_ew[0]:
        file = open('../raw_data/Arizona/'+str(county)+'/'+str(year)+'_results_county.txt', 'r')
        df_AZ = pd.DataFrame(columns = ["Year","CountyName","ContestID", "ChoiceID", "PrecinctID", "VoteTotal", "PollingPlaceVotes", "EarlyVotes", "ProvisionalVotes", "OtherVotes",
        "PartyName", "ContestName", "ChoiceName", "PrecinctDesignation", "PrecinctName", "SubJurisidiction", "VotesAllowed", "ReferendumFlag"])
        polling_places_indices = [17,23]
        early_votes_indices = [23,29]
        provisional_indices = [29,35]
        precinct_name_indices = [205,235]
        subJur_start_index = 234
        #alter for Apache
        if county == "Apache":
            if year == "2018_con":
                early_votes_indices = [17,23]
                polling_places_indices = [23,29]
            precinct_name_indices = [207,234]
        #alter for Cochise
        elif county == "Cochise":
            precinct_name_indices = [207,235]
            subJur_start_index = 235
            early_votes_indices = [17,23]
            polling_places_indices = [23,29]
        #alter for Mohave
        elif county == "Mohave" and year == "2018_con":
            early_votes_indices = [17,23]
            polling_places_indices = [23,29]
        #alter for Gila or Pima
        elif county == "Gila" or county == "Pima":
            early_votes_indices = [17,23]
            polling_places_indices = [23,29]
        #alter for Navajo
        elif county == "Navajo":
            provisional_indices = [35,41]
        #alter for Pinal
        elif county == "Pinal":
            if year == "2016_pres":
                provisional_indices = [35, 41]
            precinct_name_indices = [207,235]
        #alter for La Paz
        elif county == "La_Paz":
            early_votes_indices = [17,23]
            polling_places_indices = [23,29]
            precinct_name_indices = [207,235]
        #alter for Yuma:
        elif county == "Yuma":
            provisional_indices = [35,41]
        #parse ElectionWare nonsense formatting
        data = file.readlines()
        #rows = []
        for i in data:
            #populating other votes data per county formats
            other = 0
            #Apache other: Polling Places Votes DS200, Early Votes DS200
            if county == "Apache":
                other = int(i[35:41]) + int(i[41:47])
                #Provisional Votes DS200
                if year == "2018_con":
                    other += int(i[47:52])
            #Santa Cruz other: Polling Place Votes DS200, Early Votes DS200
            elif county == "Santa_Cruz":
                other += int(i[35:41])
                if year == "2016_pres":
                     other += int(i[41:47])
            #Navajo other: Late Early Votes
            elif county == "Navajo":
                other = int(i[29:35])
                #Conditional Provisional Votes
                if year == "pres_2016":
                    int(i[41:47])
            #Pinal other: 
            elif county == "Pinal" and year == "2016_pres":
                other = int(i[29:35])
            #Greenlee and Graham other: Provisional Votes DS200 
            elif year == "2018_con" and (county == "Greenlee" or county == "Graham"):
                other = int(i[35:40])
            #Yuma other: Late Early Votes
            elif county == "Yuma":
                other = int(i[29:35])
            rows.append({
                "Year": str(year[0:4]),
                "CountyName": county,
                "ContestID": int(i[0:4]),
                "ChoiceID": int(i[4:7]),
                "PrecinctID": int(i[7:11]),
                "VoteTotal": int(i[11:17]),
                "PollingPlaceVotes": int(i[polling_places_indices[0]:polling_places_indices[1]]),
                "EarlyVotes": int(i[early_votes_indices[0]:early_votes_indices[1]]),
                "ProvisionalVotes": int(i[provisional_indices[0]: provisional_indices[1]]),
                "PartyName": i[101:104].strip(),
                "ContestName": i[111:167].strip().lower(),
                "ChoiceName": i[167:205].strip(),
                "PrecinctDesignation": i[205:207],
                "PrecinctName": i[precinct_name_indices[0]:precinct_name_indices[1]].strip(),
                "SubJurisdiction": i[subJur_start_index:260].strip(),
                "VotesAllowed": i[260:262],
                "ReferendumFlag": i[262:264],
                "OtherVotes": other
            })
        df_AZ = df_AZ.append(rows, sort=False)
        #filter out non presidential or US House data
        df_AZ = df_AZ[df_AZ['ContestName'].str.contains('presidential electors') | df_AZ['ContestName'].str.contains('rep')]
        csv_file = '../preprocess/Arizona/election_data.csv'
        df_AZ.to_csv(path_or_buf=csv_file, index=False)
