import pandas as pd
#import os

#list of counties that use ElectionWare
counties_ew = ["Apache", "Cochise", "Gila", "Graham", "Greenlee", "Mohave", "Navajo", "Pima", "Pinal", "Santa_Cruz"]
#create csv for ew counties
#store other votes like Late Early Votes in col = 'OtherVotes'
rows = []
for county in counties_ew:
	file = open('../raw_data/Arizona/'+str(county)+'/2016_pres_results_county.txt', 'r')
	df_AZ = pd.DataFrame(columns = ["CountyName","ContestID", "ChoiceID", "PrecinctID", "VoteTotal", "PollingPlaceVotes", "EarlyVotes", "ProvisionalVotes", "OtherVotes",
 	"PartyName", "ContestName", "ChoiceName", "PrecinctDesignation", "PrecinctName", "SubJurisidiction", "VotesAllowed", "ReferendumFlag"])
	polling_places_indices = [17,23]
	early_votes_indices = [23,29]
	provisional_indices = [29,35]
	precinct_name_indices = [205,235]
	subJur_start_index = 234
	#alter for Apache
	if county == "Apache":
		precinct_name_indices = [207,234]
	#alter for Cochise
	if county == "Cochise":
		precinct_name_indices = [207,235]
		subJur_start_index = 235
	if county == "Cochise" or county == "Gila" or county == "Pima" or county == "Pinal":
		early_votes_indices = [17,23]
		polling_places_indices = [23,29]
	if county == "Navajo" or county == "Pinal":
		provisional_indices = [35,41]
	#parse ElectionWare nonsense formatting
	data = file.readlines()
	#rows = []
	for i in data:
		#populating other votes data per county formats
		other = 0
		if county == "Apache" or county == "Santa_Cruz":
			other = int(i[35:41]) + int(i[41:47])
		if county == "Navajo":
			other = int(i[29:35]) + int(i[41:47])
		rows.append({
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
			"VotesAllowed": int(i[260:262]),
			"ReferendumFlag": i[262:264],
			"OtherVotes": other
		})
df_AZ = df_AZ.append(rows, sort=False)
#filter out non presidential or US House data
df_AZ = df_AZ[df_AZ['ContestName'].str.contains('presidential electors') | df_AZ['ContestName'].str.contains('rep')]
csv_file = '../preprocess/Arizona/2016_pres.csv'
df_AZ.to_csv(path_or_buf=csv_file, index=False)
