from shapely.geometry import shape
from shapely.strtree import STRtree
import json, pickle
import pandas as pd

state_po = "AZ"

county_key = {
    "AP": "APACHE",
    "CH": "COCHISE",
    "CN": "COCONINO",
    "GI": "GILA",
    "GM": "GRAHAM",
    "GN": "GREENLEE",
    "LP": "LAPAZ",
    "MC": "MARICOPA",
    "MO": "MOHAVE",
    "NA": "NAVAJO",
    "PM": "PIMA",
    "PN": "PINAL",
    "SC": "SANTACRUZ",
    "YA": "YAVAPAI",
    "YU": "YUMA"
}

error_types = [
    "UNASSIGNED_AREA",
    "OVERLAPPING",
    "SELF_INTERSECTING",
    "ENCLOSED_PRECINCT",
    "MULTIPOLYGON",
]

df = pd.DataFrame()
df_errors = pd.DataFrame()
rows = []
errors = []

#load precinct geojson
with open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/raw_data/GeoJSON/arizona_precincts.json") as f:
    #create strTree for precincts
    for precinct in json.load(f)['features']:
        county = county_key[precinct["properties"]["cde_county"]]
        precinct_na = precinct["properties"]["precinctna"]
        uid = state_po+"_"+county+"_"+precinct_na.replace(" ", "").upper()
        bdy = precinct["geometry"]
        
        rows.append({
            "UID": uid,
            "State": state_po,
            "County": county,
            "Precinct": precinct_na,
            "BDY": bdy
        })
        if precinct["geometry"]["type"] == "MultiPolygon":
            errors.append({
                "Type": error_types[4],
                "Datasource": "data.gov",
                "PrecinctsAssociated": uid,
                "GeoJSON": bdy
            })
# precinct_tree = STRtree(precinct_poly)
df = df.append(rows, ignore_index=True)
df_errors = df_errors.append(errors, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ.csv'
df_m.to_csv(path_or_buf=csv_file, index=False)