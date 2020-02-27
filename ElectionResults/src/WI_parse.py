import pandas as pd

#get 2016_con
file = "../raw_data/Wisconsin/2016-precinct-house.csv"
WI_df = pd.read_csv(file, encoding="latin-1", low_memory=False)
	#usecols=['state_postal', 'jurisdiction', 'precinct', 'candidate_normalized', 'office'])

WI_df = WI_df[WI_df.state_postal == 'WI']
WI_df = WI_df[WI_df.office == 'US House']

WI_df.to_csv(path_or_buf='../preprocess/Wisconsin/2016_con.csv', index=False)

#get 2016_pres
file = "../raw_data/Wisconsin/2016-precinct-president.csv"
WI_df = pd.read_csv(file, encoding="latin-1", low_memory=False)
        #usecols=['state_postal', 'jurisdiction', 'precinct', 'candidate_normalized', 'office'])

WI_df = WI_df[WI_df.state_postal == 'WI']
WI_df = WI_df[WI_df.office == 'US President']

WI_df.to_csv(path_or_buf='../preprocess/Wisconsin/2016_pres.csv', index=False)

#get 2018_con
file = "../raw_data/Wisconsin/precinct_2018.csv"
WI_df = pd.read_csv(file, encoding="latin-1", low_memory=False)
        #usecols=['state_postal', 'jurisdiction', 'precinct', 'candidate_normalized', 'office'])

WI_df = WI_df[WI_df.state_po == 'WI']
WI_df = WI_df[WI_df.office == 'US House']

WI_df.to_csv(path_or_buf='../preprocess/Wisconsin/2018_con.csv', index=False)

