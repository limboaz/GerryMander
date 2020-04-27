import json
import pandas as pd

rows = []
state_properties = [("AZ", 'CD116FP'), ("OH", 'ID'), ("WI", 'District_N')]
with open("../../assets/assets/congressional_districts.json") as f:
    districts = json.load(f)
    for state, property_num in state_properties:
        print(state)
        print(property_num)
        for district in districts[state]['features']:
            num = district['properties'][property_num]
            if(state == "AZ"):
                num = num.strip('0')
            del district["properties"]
            rows.append({
                "STATE": state,
                "DISTRICT": int(num),
                "BDY": str(district).replace("\'", "\"")
            })
        
df_c = pd.DataFrame()
df_c = df_c.append(rows, ignore_index=True)

csv_file = '../CongDistrcts2.csv'
df_c.to_csv(path_or_buf=csv_file, index=False)