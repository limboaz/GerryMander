import pandas as pd

file = '../preprocess/Arizona/election_data_EW.csv'
df = pd.read_csv(file)

file = '../preprocess/Arizona/election_data_GEMS.csv'
df2 = pd.read_csv(file)

df = df.append(df2, sort=False)

file = '../preprocess/Arizona/election_data_OpenElect.csv'
df2 = pd.read_csv(file)

df = df.append(df2, sort=False)

file = '../preprocess/Arizona/election_data_WinEDS.csv'
df2 = pd.read_csv(file)

df = df.append(df2, sort=False)

combine_file = '../preprocess/Arizona/election_data_AZ.csv'
df.to_csv(path_or_buf=combine_file, index=False)