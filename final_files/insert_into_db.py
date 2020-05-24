import mysql.connector
from pprint import pprint
import json
import pandas

connection = mysql.connector.connect(
  host="35.202.163.188",
  user="isaac",
  passwd="cse416",
  database="Aztecs_prod"
)

aztecs_dev = connection.cursor(buffered=True)
state_boundaries = json.load(open("state_boundaries.json", 'r'))
state_precincts = 'final_files_%s/precincts.csv'
state_demographics = 'final_files_%s/demographics.csv'
state_election = 'final_files_%s/elections_MATCHED.csv'
state_errors = 'errors%s.csv'
state_neighbors = 'neighbors_%s.csv'
congressional_districts = pandas.read_csv('congressional_districts.csv')

states = ['AZ', 'OH', 'WI']
ElectionType = [
  "PRES",
  "CON"
]
CandidateParty = [
  "DEM", "REP", "IND", "GRN", "LIB"
]
BoundaryErrorType = [
  "UNASSIGNED_AREA",
  "OVERLAPPING",
  "SELF_INTERSECTING",
  "ENCLOSED_PRECINCT",
  "MULTIPOLYGON"
]
DataErrorType = [
	"ZERO_POPULATION",
  	"ZERO_ELECTION_DATA",
  	"VOTE_NOT_PROPORTIONAL_TO_POP",
	"MORE_VOTES_THAN_POP"
]

state_names = {'AZ': 'Arizona', 'OH': 'Ohio', 'WI': 'Wisconsin'}

insert_precinct = (
	"insert into precinct (uid, cong_district_num, congressional_district_id, county, name, precinct_geojson, state)"
	"values (%s, %s, %s, %s, %s, %s, %s)"
)

insert_state = (
	"insert into state (id, name, state_geojson)"
	"values (%s, %s, %s)"
)

insert_district = (
	"insert into congressional_district (id, congressional_district_geojson, district_num, state_code, state_id)"
	"values (%s, %s, %s, %s, %s)"
)

insert_population = (
	"insert into population_data (id, asian, black, native_american, other, pacific_islander, total, white, precinct_uid)"
	"values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
)

insert_election = (
	"insert into election_data (id, candidate, party, type, vote_total, year, precinct_uid)"
	"values (%s, %s, %s, %s, %s, %s, %s)"
)

insert_boundary_errors = (
	"insert into boundary_error (id, cong_id, data_source, type, precinct_uid, state_id, error_boundary_geojson)"
	"values (%s, %s, %s, %s, %s, %s, %s)"
)

insert_unassigned_area = (
	"insert into boundary_error (id, cong_id, data_source, type, state_id, error_boundary_geojson)"
	"values (%s, %s, %s, %s, %s, %s)"
)

insert_data_errors = (
	"insert into data_error (id, cong_id, data_source, type, precinct_uid, state_id)"
	"values (%s, %s, %s, %s, %s, %s)"
)

insert_neighbors = (
	"insert into neighbor_data (id, neighborid, precinct_uid)"
	"values (%s, %s, %s)"
)

state_to_districts = {'AZ': [], 'WI': [], 'OH': []}
duplicates = {}

pop_data_id = 0
election_data_id = 0
error_id = 0
neighbor_id = 0

def insert_csv_into_db(path, query, column_names, id_start, add_to_duplicates = False, isUID=True,execute=False):
	global duplicates
	data = []
	for _,r in pandas.read_csv(path).iterrows():
		if add_to_duplicates: duplicates[r["UID"]] = 1
		elif isUID and r["UID"] in duplicates: continue
		
		if type(id_start) == int:
			parameters = [id_start]
			id_start += 1
		else: parameters = [r[id_start]]

		for name in column_names:
			if type(name) == str:
				parameters.append(r[name])
			else: parameters.append(name(r))
		data.append(tuple(parameters))
	if execute:
		aztecs_dev.executemany(query, data)
	return id_start

population_csv_columns = ["Asian", "Black", "NativeAmerican", "Other", "PacificIslander", "Total", "White", "UID"]
precincts_csv_columns = [
	lambda a: int(a["District"]), 
	lambda a: int(str(int(a["District"])) + str(states.index(a["State"]))), 
	"County", 
	"Precinct", 
	"BDY", 
	lambda a: states.index(a["State"])
]
election_csv_columns = [
	"Candidate", 
	lambda a: CandidateParty.index(a["Party"]), 
	lambda a: ElectionType.index(a["Contest"]), 
	"VoteTotal", 
	"Year", 
	"UID"
]
for i,d in congressional_districts.iterrows():
	state_to_districts[d["STATE"]].append({"bdy": d["BDY"], "district": d["DISTRICT"]})

for state_id, state in enumerate(states):
	aztecs_dev.execute(insert_state, (int(state_id), state_names[state], json.dumps(state_boundaries[state])))

	for district in state_to_districts[state]:
		aztecs_dev.execute(insert_district, (int(str(int(district['district'])) + str(state_id)), district['bdy'], int(district['district']), int(state_id), int(state_id)))
		pass

dup_data_errors = [r for i,r in pandas.read_csv('duplicatebois/errors.csv', index_col=None).iterrows()]
dup_boundary_errors = [r for i,r in pandas.read_csv('duplicatebois/errors_mp.csv', index_col=None).iterrows()]

insert_csv_into_db('duplicatebois/precincts.csv', insert_precinct, precincts_csv_columns, "UID", True)
pop_data_id = insert_csv_into_db('duplicatebois/demographics.csv', insert_population, population_csv_columns, pop_data_id, True)
election_data_id = insert_csv_into_db('duplicatebois/elections.csv', insert_election, election_csv_columns, election_data_id, True)

boundary_errors = []
for r in dup_boundary_errors:
	duplicates[r["PrecinctsAssociated"]] = 1
	district_id = "NULL"
	if r["Type"] == "UNASSIGNED_AREA":
		district_id = int(str(int(r["districtAssociated"])) + str(states.index(r["StateId"])))
	boundary_errors.append((error_id, district_id, r["Datasource"], BoundaryErrorType.index(r["Type"]), r["PrecinctsAssociated"], states.index(r["StateID"]), r["GeoJSON"]))
	error_id+=1
aztecs_dev.executemany(insert_boundary_errors, boundary_errors)	

data_errors = []
for r in dup_data_errors:
	duplicates[r["PrecinctsAssociated"]] = 1
	data_errors.append((error_id, 0, r["Datasource"], DataErrorType.index(r["Type"]) + 5, r["PrecinctsAssociated"], states.index(r["StateID"])))
	error_id+=1
aztecs_dev.executemany(insert_data_errors, data_errors)

for state_id, state in enumerate(states[0:1]):
	print(state, "Precincts")
	insert_csv_into_db(state_precincts % state, insert_precinct, precincts_csv_columns, "UID")
	print(state, "Population")
	pop_data_id = insert_csv_into_db(state_demographics % state, insert_population, population_csv_columns, pop_data_id)
	print(state, "Election")
	election_data_id = insert_csv_into_db(state_election % state, insert_election, election_csv_columns, election_data_id, False, True, True)
	print(state, "Neighbors")
	neighbor_id = insert_csv_into_db(state_neighbors % state, insert_neighbors, ["neighborid", "precinct_uid"], neighbor_id, False, False)
	
	print(state, "Boundary Errors")
	errors = pandas.read_csv(state_errors % state)
	data_errors_data = []
	boundary_data = []
	for i,r in errors.iterrows():
		if r["PrecinctsAssociated"] in duplicates: continue
		if r["Type"] in BoundaryErrorType:
			district_id = "NULL"
			precinct = r["PrecinctsAssociated"]
			if r["Type"] == "UNASSIGNED_AREA":
				district_id = int(str(int(r["districtAssociated"])) + str(state_id))
				aztecs_dev.execute(insert_unassigned_area, (error_id, district_id, r["Datasource"], BoundaryErrorType.index(r["Type"]), state_id, r["GeoJSON"]))
			else:
				boundary_data.append((error_id, district_id, r["Datasource"], BoundaryErrorType.index(r["Type"]), precinct, state_id, r["GeoJSON"]))
				pass
		else:
			data_errors_data.append((error_id, "NULL", r["Datasource"], DataErrorType.index(r["Type"]) + 5, r["PrecinctsAssociated"], state_id))
			pass
		error_id+=1
	aztecs_dev.executemany(insert_boundary_errors, boundary_data)
	aztecs_dev.executemany(insert_data_errors, data_errors_data)

	connection.commit()

pprint(duplicates)

connection.close()