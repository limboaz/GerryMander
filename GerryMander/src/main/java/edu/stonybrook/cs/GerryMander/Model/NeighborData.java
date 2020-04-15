package edu.stonybrook.cs.GerryMander.Model;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;
import java.util.List;

@Entity
public class NeighborData {
    private long id;
    private List<String> neighbors;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public List<String> getNeighbors() {
        return neighbors;
    }

    public void setNeighbors(List<String> neighbors) {
        this.neighbors = neighbors;
    }
}
