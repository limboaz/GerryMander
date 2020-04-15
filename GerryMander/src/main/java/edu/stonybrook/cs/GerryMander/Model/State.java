package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.OneToMany;
import javax.persistence.Transient;
import java.util.List;
import java.util.Set;

public class State {
    private StatePostalCode state;
    private List<CongressionalDistrict> congressionalDistricts;
    private Set<Error> errors;

    @Enumerated(EnumType.ORDINAL)
    public StatePostalCode getState() {
        return state;
    }

    public void setState(StatePostalCode state) {
        this.state = state;
    }

    public List<CongressionalDistrict> getCongressionalDistricts() {
        return congressionalDistricts;
    }

    public void setCongressionalDistricts(List<CongressionalDistrict> congressionalDistricts) {
        this.congressionalDistricts = congressionalDistricts;
    }

    public Set<Error> getErrors() {
        return errors;
    }

    public void setErrors(Set<Error> errors) {
        this.errors = errors;
    }
}
