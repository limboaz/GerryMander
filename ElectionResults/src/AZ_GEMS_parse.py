import pandas as pd
import re

#GEM key
GEM_key = {
"PrecinctID": 1,
"PrecinctName": 2,
"ContestID": 4,
"ContestName": 5,
"ChoiceID": 13,
"ChoiceName": 14,
"PartyID": 16,
"CandidateParty": 17,
"VoteTypeID": 19,
"VoteTypeName": 20,
"VoteTotal": 22
}
#list of counties
counties_16 = ["Coconino", "La_Paz", "Yuma"]
counties_18 = ["Coconino"]
counties = [counties_16, counties_18]
#list of years
years = ["2016_pres", "2018_con"]
rows = []
index = 0
#iterate through years
for year in years:
	#iterate through each county
	for county in counties[index]:
		filename = "../raw_data/Arizona/Coconino/2016_pres_results_county.txt"
		file = open(filename, 'r')
		#parse GEMS slightly less nonsensical format
		data = file.readlines()
		for i in data:
			row = re.split('''\,(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', i)
			#add row to rows
			rows.append({
			"Year": year[0:4],
			"County": county,
			"PrecinctID": row[GEM_key["PrecinctID"]],
			"PrecinctName": row[GEM_key["PrecinctName"]],
			"ContestID": row[GEM_key["ContestID"]],
			"ContestName": row[GEM_key["ContestName"]].lower(),
			"ChoiceID": row[GEM_key["ChoiceID"]],
			"ChoiceName": row[GEM_key["ChoiceName"]],
			"PartyID": row[GEM_key["PartyID"]],
			"CandidateParty": row[GEM_key["CandidateParty"]],
			"VoteTypeID": row[GEM_key["VoteTypeID"]],
			"VoteTypeName": row[GEM_key["VoteTypeName"]],
			"VoteTotal": row[GEM_key["VoteTotal"]]
			})
	index += 1
#create dataframe
df_AZ = pd.DataFrame(rows)
#filter out non-Pres or House of Rep data
df_AZ = df_AZ[df_AZ['ContestName'].str.contains('president') | df_AZ['ContestName'].str.contains('rep')]
print(str(type(df_AZ)))
#save as csv file
csv_file = '../preprocess/Arizona/election_data_GEMS.csv'
df_AZ.to_csv(path_or_buf=csv_file, index=False)
