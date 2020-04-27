package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;

import javax.persistence.*;

@Entity
public class NeighborData {
    private long id;
    private Precinct precinct;
    private String neighborID;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }


    public String getNeighborID() {
        return neighborID;
    }

    public void setNeighborID(String neighborID) {
        this.neighborID = neighborID;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    @JsonBackReference
    public Precinct getPrecinct() {
        return precinct;
    }

    public void setPrecinct(Precinct precinct) {
        this.precinct = precinct;
    }

}
