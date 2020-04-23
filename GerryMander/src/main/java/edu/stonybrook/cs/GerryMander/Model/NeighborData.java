package edu.stonybrook.cs.GerryMander.Model;

import javax.persistence.*;
import java.util.List;

@Entity
public class NeighborData {
    private long id;
    private Precinct precinct;
    private String neighborID;
    private String testColumn;

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
    public Precinct getPrecinct() {
        return precinct;
    }

    public void setPrecinct(Precinct precinct) {
        this.precinct = precinct;
    }

    public String getTestColumn() {
        return testColumn;
    }

    public void setTestColumn(String testColumn) {
        this.testColumn = testColumn;
    }
}
