import {StatePostalCode, ElectionType, CandidateParty, ErrorType, CorrectionType} from './enums';

export interface Error {
  id: number;
  type: ErrorType;
  dataSource: string;
  errorBoundaryGeoJSON: string;
  errorValue: number;
  resolved: boolean;
  precinctUid;
  layer;
}

export interface NeighborData {
  id: number;
  neighborID: string;
}

export interface ElectionData {
  id: number;
  year: number;
  type: ElectionType;
  candidate: string;
  party: CandidateParty;
  voteTotal: number;
  precinct;
}

export interface PopulationData {
  id: number;
  total: number;
  white: number;
  black: number;
  asian: number;
  hispanic: number;
  nativeAmerican: number;
  pacificIslander: number;
  other: number;
  precinct;
}

export interface Precinct {
  uid: string;
  state: StatePostalCode;
  county: string;
  name: string;
  errors: Error[];
  neighbors: NeighborData[];
  electionData: ElectionData[];
  populationData: PopulationData;
  precinctGeoJSON;
  layer;
}

export interface CongressionalDistrict {
  id: number;
  districtNum: number;
  state: StatePostalCode;
  precincts: Precinct[];
  congressionalDistrictGeoJSON;
}

export interface Correction {
  id: number;
  type: CorrectionType;
  time;
  comment: string;
  oldValue;
  newValue;
  associatedError;
}

export interface State {
  state: StatePostalCode;
  name: string;
  congressionalDistricts: CongressionalDistrict[];
  errors: Error[];
  stateGeoJSON;
  layer;
}
