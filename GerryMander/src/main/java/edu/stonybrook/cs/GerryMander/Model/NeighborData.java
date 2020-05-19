package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;

import javax.persistence.*;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;


@Entity
public class NeighborData {
    private String id;
    private Precinct precinct;
    private String neighborID;

    public NeighborData(){}

    public NeighborData(Precinct precinct, String neighborID){
        this.precinct = precinct;
        this.neighborID = neighborID;
    }

    public NeighborData(String id, Precinct precinct, String neighborID){
        this.id = id;
        this.precinct = precinct;
        this.neighborID = neighborID;
    }

    public static List<NeighborData> mergeNeighbors(Precinct precinct, List<NeighborData> neighborA, List<NeighborData> neighborB){
        Set<NeighborData> mergedNeighbors = new HashSet<>(neighborA);
        mergedNeighbors.addAll(neighborB);
        List<NeighborData> mergedNeighborList = new ArrayList<>();
        int counter = 0;
        for(NeighborData neighbor: mergedNeighbors) {
            mergedNeighborList.add(new NeighborData(precinct.getUid() + "_NEIGHBOR_" + counter, precinct, neighbor.getNeighborID()));
        }
        return mergedNeighborList;
    }

    @Id
    @Column(length = 100)
    public String getId() {
        return id;
    }

    public void setId(String id) {
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
