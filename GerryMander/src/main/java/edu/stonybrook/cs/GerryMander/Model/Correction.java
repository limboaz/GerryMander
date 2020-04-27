package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import edu.stonybrook.cs.GerryMander.Model.Enum.CorrectionType;

import javax.persistence.*;
import java.util.Date;

@Entity
public class Correction {
    private long id;
    private CorrectionType type;
    private Date time;
    private String comment;
    private String oldValue;
    private String newValue;
    private Error associatedError;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    @Enumerated(EnumType.ORDINAL)
    public CorrectionType getType() {
        return type;
    }

    public void setType(CorrectionType type) {
        this.type = type;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public String getComment() {
        return comment;
    }

    public void setComment(String comment) {
        this.comment = comment;
    }

    public String getOldValue() {
        return oldValue;
    }

    public void setOldValue(String oldValue) {
        this.oldValue = oldValue;
    }

    public String getNewValue() {
        return newValue;
    }

    public void setNewValue(String newValue) {
        this.newValue = newValue;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "error_id")
    @JsonBackReference
    public Error getAssociatedError() {
        return associatedError;
    }

    public void setAssociatedError(Error associatedError) {
        this.associatedError = associatedError;
    }
}
