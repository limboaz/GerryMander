# get all the precincts that have no district association

import pandas as pd
from shapely.geometry import shape
import json

file = "C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ2.csv"
df_unassigned = pd.read_csv(file)
districts = [1,2,3,4,5,6,7,8,9]
df_unassigned = df_unassigned[~df_unassigned["District"].isin(districts)]
print(df_unassigned)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/CongDistrcts2.csv'
df_c = pd.read_csv(csv_file)

def get_district(bdy, state):
    districts = df_c[df_c['STATE']==state]
    precinct_bdy = shape(bdy)
    intersections = []
    for district in districts.index:
        poly_district = shape(json.loads(districts.at[district, 'BDY']))
        if precinct_bdy.intersects(poly_district):
            intersections.append((district, poly_district))
    if len(intersections) == 1:
        return districts.at[intersections[0][0], 'DISTRICT']
    # intersects multiple districts
    elif len(intersections) > 1:
        max_area = (0,0)
#         print(intersections)
        for dist_num, dist_bdy in intersections:
            intersecting_area = dist_bdy.intersection(precinct_bdy).area
#             print(dist_num)
#             print(intersecting_area)
            if(intersecting_area > max_area[1]):
                max_area = (dist_num, intersecting_area)
        return districts.at[max_area[0], 'DISTRICT']
		
def to_geojson(gap):
    return '{"type": "Feature", "geometry": '+ gap+'},'

state  = "AZ"
for precinct in df_unassigned.index:
    district = get_district(json.loads(df_unassigned.at[precinct, "BDY"]), state)
    if type(district) != 'NoneType':
        df_unassigned.at[precinct, "District"] = district
		
csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/AZ_fixedDistricts.csv'
df_unassigned.to_csv(path_or_buf=csv_file, index=False)

df_unassigned_again = df_unassigned[~df_unassigned["District"].isin(districts)]
file = open("C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/unassigned.json", "w")
for precinct in df_unassigned.index:
    file.write(to_geojson(df_unassigned.at[precinct, "BDY"]))
file.close()