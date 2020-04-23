package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import javax.persistence.*;
import java.util.List;
import java.util.Set;

@Entity
public class State {
    private StatePostalCode state;
    private String name;
    private List<CongressionalDistrict> congressionalDistricts;
    private Set<Error> errors;
    private String stateGeoJSON;

    @Id
    @Enumerated
    @Column(name = "id")
    public StatePostalCode getState() {
        return state;
    }

    public void setState(StatePostalCode state) {
        this.state = state;
    }

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @Column
    public List<CongressionalDistrict> getCongressionalDistricts() {
        return congressionalDistricts;
    }

    public void setCongressionalDistricts(List<CongressionalDistrict> congressionalDistricts) {
        this.congressionalDistricts = congressionalDistricts;
    }

    @OneToMany(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    public Set<Error> getErrors() {
        return errors;
    }

    public void setErrors(Set<Error> errors) {
        this.errors = errors;
    }

    @Lob
    public String getStateGeoJSON() {
        return stateGeoJSON;
    }

    public void setStateGeoJSON(String stateGeoJson) {
        this.stateGeoJSON = stateGeoJson;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
