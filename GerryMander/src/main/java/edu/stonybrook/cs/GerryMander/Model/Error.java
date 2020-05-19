package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonManagedReference;
import edu.stonybrook.cs.GerryMander.Model.Enum.ErrorType;

import javax.persistence.*;
import java.util.List;

@Entity
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class Error {
    protected long id;
    protected ErrorType type;
    protected String dataSource;
    protected String precinctUid;
    protected State state;
    protected String congId;
    protected List<Correction> corrections;
    protected Boolean isResolved;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    @Enumerated(EnumType.ORDINAL)
    public ErrorType getType() {
        return type;
    }

    public void setType(ErrorType type) {
        this.type = type;
    }

    public String getDataSource() {
        return dataSource;
    }

    public void setDataSource(String dataSource) {
        this.dataSource = dataSource;
    }

    public String getPrecinctUid() {
        return precinctUid;
    }

    public void setPrecinctUid(String precinctUid) {
        this.precinctUid = precinctUid;
    }

    @OneToMany(mappedBy = "associatedError", cascade = CascadeType.ALL)
    @JsonManagedReference
    public List<Correction> getCorrections() {
        return corrections;
    }

    public void setCorrections(List<Correction> corrections) {
        this.corrections = corrections;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "state_id")
    @JsonBackReference
    public State getState() {
        return state;
    }

    public void setState(State state) {
        this.state = state;
    }

    public String getCongId(){ return this.congId; }

    public void setCongId(String congID){ this.congId = congID; }

    public Boolean isResolved(){ return this.isResolved; }

    public void setResolved(Boolean status){ this.isResolved = status; }
}