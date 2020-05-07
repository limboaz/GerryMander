from shapely.geometry import shape
import json, pickle
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

csv_file = '../preprocessing/CongDistrcts.csv'
df_c = pd.read_csv(csv_file)

def get_district(bdy, state):
    districts = df_c[df_c['STATE']==state]
    precinct_bdy = shape(bdy)
    for district in districts.index:
        jsonify = districts.at[district, 'BDY']
        poly_district = json.loads(jsonify)
        poly_district = shape(poly_district["geometry"])
        if precinct_bdy.within(poly_district):
            return districts.at[district, 'DISTRICT']
            
def to_geojson(gap):
    return '{"type": "Feature", "geometry": {"type": "'+str(gap.geom_type)+'", "coordinates": ['+str(list(gap.exterior.coords))+']}},'

#load precinct geojson
precincts_bdy = []
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
            "BDY": str(precinct).replace("\'", "\"")
        })
        precincts_bdy.append(shape(precinct["geometry"]))
        if precinct["geometry"]["type"] == "MultiPolygon":
            errors.append({
                "Type": error_types[4],
                "Datasource": "data.gov",
                "PrecinctsAssociated": uid,
                "GeoJSON": str(precinct).replace("\'", "\"")
            })
precinct_tree = STRtree(precincts_bdy)
index_by_id = dict((id(poly), i) for i, poly in enumerate(precincts_bdy))
df = df.append(rows, ignore_index=True)
df_errors = df_errors.append(errors, ignore_index=True)

csv_file = '../preprocessing/AZ.csv'
df_m.to_csv(path_or_buf=csv_file, index=False)

# save strTree and indexing
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/strtree_precincts.pkl", "wb")
pickle.dump(precinct_tree, file)
file.close()
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/index_precincts.pkl", "wb")
pickle.dump(index_by_id, file)
file.close()

#Enclosed Precincts
enclosed_errors = []
for enclosed_id, enclosed in enumerate(precincts_bdy):
    closest = precinct_tree.query(enclosed)
    # iterate through the query result to find precincts with relationships with current precinct
    intersections = 0
    for outer_id, outer in closest:
        if enclosed.intersects(outer) and not enclosed.equals(outer):
            intersections = intersections + 1
    # check if current precinct is enclosed precinct
    if intersections == 1:    
        enclosed_errors.append({
            "Type": error_types[3],
            "Datasource": "data.gov",
            "PrecinctsAssociated": df.at[enclosed_id, "UID"],
            "GeoJSON": df.at[enclosed_id, "BDY"]
        })
if len(enclosed_errors) != 0:
    df_errors = df_errors.append(enclosed_errors, ignore_index=True)  
    
#overlapping precincts
overlap_errors = []
for precinct_id, precinct in enumerate(precincts_bdy):
    closest = [(index_by_id[id(poly)], poly) for poly in precinct_tree.query(precinct)]
    # iterate through the query result to find precincts with relationships with current precinct
    for overlap_id, overlap in closest:
        # TODO: buffer of 200 feet
        if precinct.overlaps(overlap): 
                overlap_errors.append({
                "Type": error_types[1],
                "Datasource": "data.gov",
                "PrecinctsAssociated": [df.at[precinct_id, "UID"], df.at[overlap_id, "UID"]],
                "GeoJSON": precinct.intersection(overlap)
            })
print(len(overlap_errors))
if len(overlap_errors) != 0:
    df_errors = df_errors.append(overlap_errors, ignore_index=True)  

#gaps
precicnt_union = unary_union(precincts_bdy)
state_bdy = ""
with open("C:/Users/mlo10/IdeaProjects/GerryMander/assets/assets/us_states_500K.json") as f:
    for state in json.load(f)['features']:
        if state["properties"]["STUSPS"] == state_po:
            state_bdy = shape(state["geometry"])
            break
print(state_bdy == "")
gaps = state_bdy.difference(precicnt_union)

gaps_list = []

for gap in gaps:
    bdy = to_geojson(gap)
    gaps_list.append({
        "Type": error_types[0],
        "Datasource": "data.gov",
        "PrecinctsAssociated": "",
        "GeoJSON": bdy
    })
print(gaps_list)
# create geojson of gaps
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/gaps.json", "w")
for gap in gaps_list:
    file.write(gap["GeoJSON"])
file.close()

#why were some disrticts not found
districts = [1,2,3,4,5,6,7,8,9]
df_failed = df[~df['District'].isin(districts)]
print(df_failed)

# election errors
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_FAILED.csv'
df_failed.to_csv(path_or_buf=csv_file, index=False)
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ.csv'
# df_ed = pd.read_csv(file, usecols=["UID", "State", "County", "Precinct"])
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

csv_file = '../preprocessing/AZ_errors.csv'
df.to_csv(path_or_buf=csv_file, index=False)

file = '../../ElectionResults/preprocess/ELECTION_DATA/election_data_AZ.csv'
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

csv_file = '../preprocessing/AZ_data_errors.csv'
df_data_errors.to_csv(path_or_buf=csv_file, index=False)