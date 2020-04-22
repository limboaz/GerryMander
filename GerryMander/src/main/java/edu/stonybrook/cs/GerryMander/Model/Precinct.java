package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import javax.persistence.*;
import java.util.List;
import java.util.Objects;

@Entity
@Table(name = "precinct")
public class Precinct {
    private String uid;
    private StatePostalCode state;
    private int congDistrictNum;
    private CongressionalDistrict congressionalDistrict;
    private String county;
    private String name;
    private List<Error> errors;
    private List<ElectionData> electionData;
    private PopulationData populationData;
    private String precinctGeoJSON;
    private List<NeighborData> neighbors;
    private long totalPopulation;

    public Precinct(){

    }

    public Precinct(String uid){
        this.uid = uid;
    }

    @Id
    @Column(name = "uid", length = 100)
    public String getUid() {
        return uid;
    }

    public void setUid(String uid) {
        this.uid = uid;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    public CongressionalDistrict getCongressionalDistrict() {
        return congressionalDistrict;
    }

    public void setCongressionalDistrict(CongressionalDistrict congressionalDistrict) {
        this.congressionalDistrict = congressionalDistrict;
    }

    @Enumerated(EnumType.ORDINAL)
    public StatePostalCode getState() {
        return state;
    }

    public void setState(StatePostalCode state) {
        this.state = state;
    }

    public int getCongDistrictNum() {
        return congDistrictNum;
    }

    public void setCongDistrictNum(int congDistrictNum) {
        this.congDistrictNum = congDistrictNum;
    }

    public String getCounty() {
        return county;
    }

    public void setCounty(String county) {
        this.county = county;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @OneToMany(mappedBy = "precinct", cascade = CascadeType.ALL)
    public List<Error> getErrors() {
        return errors;
    }

    public void setErrors(List<Error> errors) {
        this.errors = errors;
    }

    @OneToMany(mappedBy = "precinct", cascade = CascadeType.ALL)
    public List<ElectionData> getElectionData() {
        return electionData;
    }

    public void setElectionData(List<ElectionData> electionData) {
        this.electionData = electionData;
    }

    @OneToOne(mappedBy = "precinct", cascade = CascadeType.ALL)
    public PopulationData getPopulationData() {
        return populationData;
    }

    public void setPopulationData(PopulationData populationData) {
        this.populationData = populationData;
    }

    @Lob
    public String getPrecinctGeoJSON() {
        return precinctGeoJSON;
    }

    public void setPrecinctGeoJSON(String precinctGeoJSON) {
        this.precinctGeoJSON = precinctGeoJSON;
    }

    @OneToMany(mappedBy = "precinct", cascade = CascadeType.ALL)
    public List<NeighborData> getNeighbors() {
        return neighbors;
    }

    public void setNeighbors(List<NeighborData> neighbors) {
        this.neighbors = neighbors;
    }

    public long getTotalPopulation() {
        return totalPopulation;
    }

    public void setTotalPopulation(long totalPopulation) {
        this.totalPopulation = totalPopulation;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Precinct precinct = (Precinct) o;
        return uid.equals(precinct.uid);
    }

    @Override
    public int hashCode() {
        return Objects.hash(uid);
    }
}
