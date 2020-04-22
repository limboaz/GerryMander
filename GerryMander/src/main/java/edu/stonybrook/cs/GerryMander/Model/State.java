package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import javax.persistence.*;
import javax.websocket.ClientEndpoint;
import java.util.List;
import java.util.Set;

@Entity
public class State {

    private StatePostalCode state;

    private List<CongressionalDistrict> congressionalDistricts;

    private Set<Error> errors;

    @Id
    @Enumerated
    @Column(name = "id")
    public StatePostalCode getState() {
        return state;
    }

    public void setState(StatePostalCode state) {
        this.state = state;
    }

    @OneToMany(mappedBy = "state", cascade = CascadeType.ALL)
    @Column
    public List<CongressionalDistrict> getCongressionalDistricts() {
        return congressionalDistricts;
    }

    public void setCongressionalDistricts(List<CongressionalDistrict> congressionalDistricts) {
        this.congressionalDistricts = congressionalDistricts;
    }

    @OneToMany(mappedBy = "state")
    @Column
    public Set<Error> getErrors() {
        return errors;
    }

    public void setErrors(Set<Error> errors) {
        this.errors = errors;
    }
}
