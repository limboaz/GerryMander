package edu.stonybrook.cs.GerryMander.Model;

import javax.persistence.*;
import java.util.List;

@Entity
@Table(name = "NeighborData")
public class NeighborData {
    private long id;
    private String precinct1;
    private String precinct2;
    private Precinct precinct;

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

    public String getPrecinct2() {
        return precinct2;
    }

    public void setPrecinct2(String precinct2) {
        this.precinct2 = precinct2;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    public Precinct getPrecinct() {
        return precinct;
    }

    public void setPrecinct(Precinct precinct) {
        this.precinct = precinct;
    }
}
