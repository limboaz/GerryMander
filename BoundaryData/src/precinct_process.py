from shapely.geometry import shape
import json
import pandas as pd


county_map = {
    0:"Arizona",
    1:"Apache",
    3:"Cochise",
    5:"Coconino",
    7:"Gila",
    9:"Graham",
    11:"Greenlee",
    12:"La Paz",
    13:"Maricopa",
    15:"Mohave",
    17:"Navajo",
    19:"Pima",
    21:"Pinal",
    23:"Santa Cruz",
    25:"Yavapai",
    27:"Yuma"
}

error_types = [
    "UNASSIGNED_AREA",
    "OVERLAPPING",
    "SELF_INTERSECTING",
    "ENCLOSED_PRECINCT",
    "MULTIPOLYGON",
]

state_po = "AZ"

df = pd.DataFrame()
df_errors = pd.DataFrame()
rows = []
errors = []

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/CongDistrcts.csv'
df_c = pd.read_csv(csv_file)

def get_district(bdy, state):
    districts = df_c[df_c['STATE']==state]
    precinct_bdy = shape(bdy)
    for district in districts.index:
        jsonify = districts.at[district, 'BDY'].replace("\'", "\"")
        poly_district = json.loads(jsonify)
        poly_district = shape(poly_district["geometry"])
        if precinct_bdy.within(poly_district):
            return districts.at[district, 'DISTRICT']

#load precinct geojson
with open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/raw_data/GeoJSON/arizona.json") as f:
    #create strTree for precincts
    for precinct in json.load(f)['features']:
        county = county_map[int(precinct["properties"]["county"].lstrip("0"))]
        precinct_na = precinct["properties"]["name"]
        uid = state_po+"_"+county.replace(" ", "").upper()+"_"+precinct_na.replace(" ", "").upper()
        del precinct["properties"]
        del precinct["id"]
        rows.append({
            "UID": uid,
            "State": state_po,
            "County": county,
            "Precinct": precinct_na,
            "District": get_district(precinct["geometry"], state_po),
            "BDY": precinct
        })
        if precinct["geometry"]["type"] == "MultiPolygon":
            errors.append({
                "Type": error_types[4],
                "Datasource": "data.gov",
                "PrecinctsAssociated": uid,
                "GeoJSON": precinct
            })
df = df.append(rows, ignore_index=True)
df_errors = df_errors.append(errors, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ.csv'
df_m.to_csv(path_or_buf=csv_file, index=False)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_errors.csv'
df.to_csv(path_or_buf=csv_file, index=False)

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ.csv'
ed = pd.read_csv(file, usecols=["UID"]).UID.unique()

df_data_errors = pd.DataFrame()
data_errors = []

#find election data errors
df_zero_elec = df[~df["UID"].isin(ed)]
#create errors
for precinct in df_zero_elec.index:
    data_errors.append({
        "Type": error_types[6],
        "Datasource": "data.gov",
        "PrecinctsAssociated": df_zero_elec.at[precinct, "UID"],
        "ErrorValue": 0.0
    })
    
df_data_errors = df_data_errors.append(data_errors, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_data_errors.csv'
df_data_errors.to_csv(path_or_buf=csv_file, index=False)