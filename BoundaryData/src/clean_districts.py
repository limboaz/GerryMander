from shapely.geometry import shape
import json
import pandas as pd

rows = []
with open("C:/Users/mlo10/IdeaProjects/GerryMander/assets/assets/congressional_districts.json") as f:
    districts = json.load(f)
    for district in districts['WI']['features']:
        rows.append({
            "STATE": "WI",
            "DISTRICT": int(district['properties']['District_N']),
            "BDY": district['geometry']
        })
    for district in districts['OH']['features']:
        rows.append({
            "STATE": "OH",
            "DISTRICT": int(district['properties']['ID']),
            "BDY": district['geometry']
        })
        
    for district in districts['AZ']['features']:
        rows.append({
            "STATE": "AZ",
            "DISTRICT": int(district['properties']['CD116FP'].strip('0')),
            "BDY": district['geometry']
        })
        
df_c = pd.DataFrame()
df_c = df_c.append(rows, ignore_index=True)

csv_file = 'C:/Users/mlo10/IdeaProjects/GerryMander/BoundaryData/CongDistrcts.csv'
df_c.to_csv(path_or_buf=csv_file, index=False)