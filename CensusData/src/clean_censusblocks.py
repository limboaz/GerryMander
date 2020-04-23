from shapely.geometry import shape
import json, os
import pandas as pd

# delete census blocks that have zero population
# load block data from csv
file_path = "../raw_data/Arizona/census_blocks"
demo_files = list(os.listdir(file_path))
df_demos = pd.DataFrame()
rows_to_rm = []
for file in demo_files:
    print(file)
    file = file_path+"/"+file
    df_demo = pd.read_csv(file, dtype = {"Total:": int})
    #make Id match block bdy format
    df_demo["Id"] = df_demo["Id"].map(lambda x: x.lstrip('1000000US'))
    # record block ids that have zero population
    rows_to_rm = list(df_demo[df_demo["Total:"] == 0]["Id"])
    # remove blocks from dataframe
    df_demo = df_demo[~df_demo["Id"].isin(rows_to_rm)]
    # add to df_demos
    df_demos = df_demos.append(df_demo, ignore_index = True)

#remove not needed col
df_cols_rm = list(df_demo.columns)[12:]
df_cols_rm = df_cols_rm + ["Id2","Geography", "Population of one race:"]
df_demos = df_demos.drop(columns = df_cols_rm)
# rename col to match project db attributes
df_demos = df_demos.rename(columns={
             "Population of one race: - White alone" : "White",
             "Population of one race: - Black or African American alone" : "Black",
             "Population of one race: - Asian alone" : "Asian",
             "Population of one race: - American Indian and Alaska Native alone" : "NativeAmerican",
             "Population of one race: - Native Hawaiian and Other Pacific Islander alone" : "PacificIslander"
            })

# keep only the fields we care about in census data
# initialize new col for misc demographic cols
df_demos["Other"] = 0
# other demo col names
other_cols = ["Population of one race: - Some Other Race alone", "Two or More Races:"]
# populate other
for block in df_demos.index:
    other = 0
    for col in other_cols:
        other += df_demos.at[block, col]
    df_demos.at[block, "Other"] = other
# delete other cols that are now aggregated into other
df_demos = df_demos.drop(columns = other_cols)

csv_file = '../AZ_pop_blocks.csv'
df_demos.to_csv(path_or_buf=csv_file, index=False)

blocks_gj = ""
#load census block geojson
with open("C:../raw_data/Geography/GeoJSON/censusblock_az.json") as f:
    blocks_gj = json.load(f)["features"]

# save block bdy data in csv
df_b = pd.DataFrame()
blocks = []
for censusblock in blocks_gj:
    block_id = censusblock["properties"]["BLOCKID10"]
    del censusblock["properties"]
    blocks.append({
        "BlockID": block_id,
        "BDY": str(censusblock).replace("\'", "\"")
    })
df_b = df_b.append(blocks, ignore_index =True)
# remove blocks from block bdy dataframe
df_b = df_b[df_b["BlockID"].isin(rows_to_rm)]

csv_file = '../AZ_blocks.csv'
df_b.to_csv(path_or_buf=csv_file, index=False)