package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import java.util.List;
import java.util.Set;

public class Precinct {
    String uid;
    StatePostalCode state;
    String county;
    CongressionalDistrict congressionalDistrict;
    String name;
    List<Error> errors;
    List<ElectionData> electionData;
    PopulationData populationData;
    String precinctGeoJSON;
    Set<NeighborData> neighbors;
    long totalPopulation;
}
