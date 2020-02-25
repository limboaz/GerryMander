import pandas as pd

file = "../raw_data/Wisconsin/2016-precinct-house.csv"
WI_df = pd.read_csv(file, encoding="latin-1", low_memory=False)
	#usecols=['state_postal', 'jurisdiction', 'precinct', 'candidate_normalized', 'office'])

WI_df = WI_df[WI_df.state_postal == 'WI']
WI_df = WI_df[WI_df.office == 'US House']

WI_df.to_csv(path_or_buf='WI_congress.csv', index=False)
