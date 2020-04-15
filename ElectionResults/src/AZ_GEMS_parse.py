import pandas as pd
import re

def strip_quotes(str):
	return str.strip("\"")


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
		filename = "../raw_data/Arizona/"+county+"/"+year+"_results_county.txt"
		file = open(filename, 'r')
		#parse GEMS slightly less nonsensical format
		data = file.readlines()
		for i in data:
			# print(i)
			row = re.split('''\,(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', i)
			row = list(map(strip_quotes, row))
			#check if vote type is VoteTotal and only candidate stats (not NP voteType)
			# print(str(row[GEM_key["CandidateParty"]]))
			# print("NP")
			# exit(0)
			if int(row[GEM_key["VoteTypeID"]]) == 999999 and row[GEM_key["CandidateParty"]] != "NP":
				#add row to rows
				rows.append({
					"UID": str("AZ_"+re.sub(r" |_", "", county)+"_"+str(row[GEM_key["PrecinctName"]]).replace(" ", "")).upper(),
					"State": "AZ",
					"County": county,
					"Precinct": row[GEM_key["PrecinctName"]],
					"Year": year[0:4],
					"Contest": row[GEM_key["ContestName"]].lower(),
					"Party": row[GEM_key["CandidateParty"]],
					"Candidate": row[GEM_key["ChoiceName"]],
					"VoteTypeName": row[GEM_key["VoteTypeName"]],
					"VoteTotal": row[GEM_key["VoteTotal"]]
				})
	index += 1
#create dataframe
df_AZ = pd.DataFrame(rows)
#filter out non-Pres or House of Rep data
df_AZ = df_AZ[df_AZ['Contest'].str.contains('president') | df_AZ['Contest'].str.contains('rep')]
#save as csv file
csv_file = '../preprocess/Arizona/election_data_GEMS2.csv'
df_AZ.to_csv(path_or_buf=csv_file, index=False)
