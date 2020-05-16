#!/usr/bin/env python
# coding: utf-8

# In[1]:


from shapely.geometry import shape
from shapely.strtree import STRtree
from shapely.ops import unary_union
import json, pickle, csv
import pandas as pd

error_types = [
    "UNASSIGNED_AREA",
    "OVERLAPPING",
    "SELF_INTERSECTING",
    "ENCLOSED_PRECINCT",
    "MULTIPOLYGON",
    "ZERO_POPULATION",
    "ZERO_ELECTION_DATA",
    "VOTE_NOT_PROPORTIONAL_TO_POP"
]


# In[112]:


state_po = "OH"

# get fip code to county name mapping
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_fip.csv'
fips = csv.reader(open(file, 'r'))
county_map = {}
for row in fips:
   key, value = row
   county_map[int(key)] = value
print(county_map)


# In[127]:


df = pd.DataFrame()
df_errors = pd.DataFrame()
rows = []
errors = []


# In[128]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/CongDistrcts2.csv'
df_c = pd.read_csv(csv_file)
df_c = df_c[df_c['STATE']==state_po]
districts = pd.DataFrame()
districts = districts.append(df_c, ignore_index=True)
districts_bdy = []
for district in districts.index:
    districts_bdy.append(shape(json.loads(districts.at[district, 'BDY'])))
district_tree = STRtree(districts_bdy)
print(districts)


# In[129]:


index_by_id_dist = dict((id(poly), i) for i, poly in enumerate(districts_bdy))


# In[130]:


def get_district(bdy, state):
    precinct_bdy = shape(bdy)
    closest = [(index_by_id_dist[id(poly)], poly) for poly in district_tree.query(precinct_bdy)]
    for dist_num, dist_bdy in closest:
        if precinct_bdy.within(dist_bdy):
            return districts.at[dist_num, 'DISTRICT']


# In[132]:


#load precinct geojson
precincts_bdy = []
with open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/raw_data/GeoJSON/ohio.json") as f:
    #create strTree for precincts
    for precinct in json.load(f)['features']:
        precinct_na = precinct["properties"]["name"]
        precinct_bdy = precinct["geometry"]
        # ghost precinct
        if precinct_na.upper() == "WATER":
            errors.append({
                "Type": error_types[0],
                "Datasource": "data.gov",
                "PrecinctsAssociated": "",
                "GeoJSON": json.dumps(precinct_bdy)
            })
#             del precinct["properties"]
#             del precinct["id"]
        else:
            county = county_map[int(precinct["properties"]["county"].lstrip("0"))]
            uid = state_po+"_"+county.replace(" ", "").upper()+"_"+precinct_na.replace(" ", "").upper()
#             del precinct["properties"]
#             del precinct["id"]
            rows.append({
                "UID": uid,
                "State": state_po,
                "County": county,
                "Precinct": precinct_na,
                "District": get_district(precinct_bdy, state_po),
                "BDY": json.dumps(precinct_bdy)
            })
            precincts_bdy.append(shape(precinct_bdy))
            if precinct_bdy["type"] == "MultiPolygon":
                errors.append({
                    "Type": error_types[4],
                    "Datasource": "data.gov",
                    "PrecinctsAssociated": uid,
                    "GeoJSON": json.dumps(precinct_bdy)
                })
precinct_tree = STRtree(precincts_bdy)
index_by_id = dict((id(poly), i) for i, poly in enumerate(precincts_bdy))
df = df.append(rows, ignore_index=True)
df_errors = df_errors.append(errors, ignore_index=True)



# In[133]:


# save strTree and indexing
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/precincts_OH.pkl", "wb")
pickle.dump(precincts_bdy, file)
file.close()
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/strtree_precincts_OH.pkl", "wb")
pickle.dump(precinct_tree, file)
file.close()
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/index_precincts_OH.pkl", "wb")
pickle.dump(index_by_id, file)
file.close()


# In[141]:


print(df_errors[df_errors["Type"]=="UNASSIGNED_AREA"])


# In[135]:


# get all the precincts that have no district association
# list of districts in OH. Will vary for all states
dist_list = [-1,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
df_unassigned = df[~df["District"].isin(dist_list)]

def get_district_ua(bdy, state):
    precinct_bdy = shape(bdy)
    intersections = []
    closest = [(index_by_id_dist[id(poly)], poly) for poly in district_tree.query(precinct_bdy)]
    for district, poly_district in closest:
        if precinct_bdy.intersects(poly_district):
            intersections.append((district, poly_district))
    if len(intersections) == 1:
        return districts.at[intersections[0][0], 'DISTRICT']
    # intersects multiple districts
    elif len(intersections) > 1:
        max_area = (-1,0)
#         print(intersections)
        for dist_num, dist_bdy in intersections:
            if not dist_bdy.is_valid:
                dist_bdy = max(dist_bdy, key=lambda a: a.area).buffer(0)
#                 if not dist_bdy.is_valid:
#                     return None
#             else:
            intersecting_area = dist_bdy.intersection(precinct_bdy).area
            if(intersecting_area > max_area[1]):
                max_area = (dist_num, intersecting_area)
        if max_area[0] != -1:
            return districts.at[max_area[0], 'DISTRICT']


# In[136]:


for precinct in df_unassigned.index:
    district = get_district_ua(json.loads(df_unassigned.at[precinct, "BDY"]), state_po)
    if type(district) != 'NoneType':
        df_unassigned.at[precinct, "District"] = district


# In[137]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_fixedDistricts.csv'
df_unassigned.to_csv(path_or_buf=csv_file, index=False)


# In[139]:


#Enclosed Precincts
enclosed_errors = []
for enclosed_id, enclosed in enumerate(precincts_bdy):
    closest = precinct_tree.query(enclosed)
    # iterate through the query result to find precincts with relationships with current precinct
    intersections = 0
    for outer in closest:
        if enclosed.intersects(outer) and not enclosed.equals(outer):
            intersections = intersections + 1
    # check if current precinct is enclosed precinct
    if intersections == 1:   
        # add new entry in df_errors
        enclosed_errors.append({
            "Type": error_types[3],
            "Datasource": "data.gov",
            "PrecinctsAssociated": df.at[enclosed_id, "UID"],
            "GeoJSON": df.at[enclosed_id, "BDY"]
        })
if len(enclosed_errors) != 0:
    df_errors = df_errors.append(enclosed_errors, ignore_index=True)  


# In[140]:


print(df_errors)


# In[108]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_errors.csv'
df_errors.to_csv(path_or_buf=csv_file, index=False)


# In[138]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_bdy.csv'
df.to_csv(path_or_buf=csv_file, index=False)


# In[142]:


csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/OH_errors.csv'
df_errors.to_csv(path_or_buf=csv_file, index=False)


# In[143]:


#overlapping precincts
overlap_errors = []
for precinct_id, precinct in enumerate(precincts_bdy):
    closest = [(index_by_id[id(poly)], poly) for poly in precinct_tree.query(precinct)]
    # iterate through the query result to find precincts with relationships with current precinct
    for overlap_id, overlap in closest:
        if precinct.overlaps(overlap):
            overlap_errors.append({
            "Type": error_types[1],
            "Datasource": "data.gov",
            "PrecinctsAssociated": [df.at[precinct_id, "UID"], df.at[overlap_id, "UID"]],
            "GeoJSON": precinct.intersection(overlap)
            })
print(len(overlap_errors))
if len(enclosed_errors) != 0:
    df_errors = df_errors.append(enclosed_errors, ignore_index=True)


# In[144]:


#gaps
districts = df_c[df_c['STATE']==state]
precicnt_union = unary_union(precincts_bdy)


# In[145]:


state_bdy = ""
with open("C:/Users/mlo10/IdeaProjects/GerryMander/assets/assets/us_states_500K.json") as f:
    for state in json.load(f)['features']:
        if state["properties"]["STUSPS"] == state_po:
            state_bdy = shape(state["geometry"])
            break
print(state_bdy == "")


# In[154]:


gaps = precicnt_union.symmetric_difference(state_bdy)


# In[155]:


def to_geojson(gap):
    return '{"type": "Feature", "geometry": {"type": "'+str(gap.geom_type)+'", "coordinates": ['+str(list(gap.exterior.coords))+']}},'


# In[156]:


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


# In[157]:


file = open("C:/Users/mlo10/IdeaProjects/GerryMander/gaps_OH3.json", "w")
for gap in gaps_list:
    file.write(gap["GeoJSON"])
file.close()


# In[3]:

# election errors
file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_bdy2.csv'
df_bdy2 = pd.read_csv(file, usecols=["UID"])

file = 'C:/Users/mlo10/IdeaProjects/GerryMander/ElectionResults/preprocess/ELECTION_DATA/election_data_AZ.csv'
# df_ed = pd.read_csv(file, usecols=["UID", "State", "County", "Precinct"])
ed = pd.read_csv(file, usecols=["UID"]).UID.unique()

df_data_errors = pd.DataFrame()
data_errors = []

#find election data errors
df_zero_elec = df_bdy2[~df_bdy2["UID"].isin(ed)]
#create errors
for precinct in df_zero_elec.index:
    data_errors.append({
        "Type": error_types[6],
        "Datasource": "azsos.gov",
        "PrecinctsAssociated": df_zero_elec.at[precinct, "UID"],
        "ErrorValue": 0.0
    })
    
df_data_errors = df_data_errors.append(data_errors, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_data_errors.csv'
df_data_errors.to_csv(path_or_buf=csv_file, index=False)