package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.ErrorType;

import javax.persistence.*;
import java.util.Set;

@Entity
public abstract class Error {
    protected long id;
    protected ErrorType type;
    protected String dataSource;
    protected Set<Precinct> precinctsAssociated;

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

    @OneToMany
    public Set<Precinct> getPrecinctsAssociated() {
        return precinctsAssociated;
    }

    public void setPrecinctsAssociated(Set<Precinct> precinctsAssociated) {
        this.precinctsAssociated = precinctsAssociated;
    }
}
