package edu.stonybrook.cs.GerryMander.Model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.util.List;

@Entity
public class NeighborData {
    private long id;
    private String precinct1;
    private String preicnct2;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getPrecinct1() {
        return precinct1;
    }

    public void setPrecinct1(String precinct1) {
        this.precinct1 = precinct1;
    }

    public String getPreicnct2() {
        return preicnct2;
    }

    public void setPreicnct2(String preicnct2) {
        this.preicnct2 = preicnct2;
    }
}
