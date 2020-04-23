package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;

import javax.persistence.*;
import java.util.List;

@Entity
public class CongressionalDistrict {
    private long id;
    private int districtNum;
    private StatePostalCode stateCode;
    private List<Precinct> precincts;
    private String congressionalDistrictGeoJSON;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public int getDistrictNum() {
        return districtNum;
    }

    public void setDistrictNum(int districtNum) {
        this.districtNum = districtNum;
    }

    @Enumerated
    public StatePostalCode getStateCode() {
        return stateCode;
    }

    public void setStateCode(StatePostalCode stateCode) {
        this.stateCode = stateCode;
    }

    @OneToMany(mappedBy = "congressionalDistrict", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    public List<Precinct> getPrecincts() {
        return precincts;
    }

    public void setPrecincts(List<Precinct> precincts) {
        this.precincts = precincts;
    }

    @Lob
    public String getCongressionalDistrictGeoJSON() {
        return congressionalDistrictGeoJSON;
    }

    public void setCongressionalDistrictGeoJSON(String congressionalDistrictGeoJSON) {
        this.congressionalDistrictGeoJSON = congressionalDistrictGeoJSON;
    }
}
