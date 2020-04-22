package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.ErrorType;

import javax.persistence.*;
import java.util.List;
import java.util.Set;

@Entity
@Table(name = "error")
@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)
public abstract class  Error {
    protected long id;
    protected ErrorType type;
    protected String dataSource;
    protected Precinct precinct;
    protected State state;
    protected List<Correction> corrections;

    @Id
    @Column(name = "id")
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

    @ManyToOne(fetch = FetchType.LAZY)
    public Precinct getPrecinct() {
        return precinct;
    }

    public void setPrecinct(Precinct precinct) {
        this.precinct = precinct;
    }

    @OneToMany(mappedBy = "associatedError", cascade = CascadeType.ALL)
    public List<Correction> getCorrections() {
        return corrections;
    }

    public void setCorrections(List<Correction> corrections) {
        this.corrections = corrections;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    public State getState() {
        return state;
    }

    public void setState(State state) {
        this.state = state;
    }
}
