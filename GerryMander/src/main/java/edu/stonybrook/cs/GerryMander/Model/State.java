package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonManagedReference;
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

    @OneToMany(mappedBy = "state", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JsonManagedReference
    public List<CongressionalDistrict> getCongressionalDistricts() {
        return congressionalDistricts;
    }

    public void setCongressionalDistricts(List<CongressionalDistrict> congressionalDistricts) {
        this.congressionalDistricts = congressionalDistricts;
    }

    @OneToMany(mappedBy = "state", fetch = FetchType.LAZY)
    @JsonManagedReference
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