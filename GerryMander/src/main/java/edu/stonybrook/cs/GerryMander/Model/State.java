package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import java.util.List;
import java.util.Set;

public class State {
    StatePostalCode state;
    List<Precinct> precincts;
    List<CongressionalDistrict> congressionalDistricts;
    Set<Error> errors;
}
