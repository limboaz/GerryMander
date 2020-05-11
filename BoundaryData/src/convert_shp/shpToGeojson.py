import fiona
import json
from pprint import pprint

features = []
crs = None
with fiona.collection("tl_2012_39_vtd10/tl_2012_39_vtd10.shp", "r") as source:
    for feat in source:
        pprint(feat['properties']["NAME10"])
        county = feat['properties']["COUNTYFP10"]
        state = feat['properties']["STATEFP10"]
        name = feat['properties']["NAME10"]
        feat['properties'].clear()
        feat['properties'].update(
            county=county,
            state=state,
            name=name) # with your attributes
        features.append(feat)
    crs = " ".join("+%s=%s" % (k,v) for k,v in source.crs.items())

my_layer = {
    "type": "FeatureCollection",
    "features": features,
    "crs": {
        "type": "link", 
        "properties": {"href": "my_layer.crs", "type": "proj4"} }}

with open("my_layer.json", "w") as f:
    f.write(json.dumps(my_layer))
with open("my_layer.crs", "w") as f:
    f.write(crs)