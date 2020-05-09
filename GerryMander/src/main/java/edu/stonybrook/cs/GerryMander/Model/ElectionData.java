package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import edu.stonybrook.cs.GerryMander.Model.Enum.CandidateParty;
import edu.stonybrook.cs.GerryMander.Model.Enum.ElectionType;

import javax.persistence.*;

@Entity
@JsonIgnoreProperties("precinct")
public class ElectionData {
    private long id;
    private int year;
    private ElectionType type;
    private String candidate;
    private CandidateParty party;
    private int voteTotal;
    private Precinct precinct;

    @Id
    @GeneratedValue
    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    @Enumerated(EnumType.ORDINAL)
    public ElectionType getType() {
        return type;
    }

    public void setType(ElectionType type) {
        this.type = type;
    }

    public String getCandidate() {
        return candidate;
    }

    public void setCandidate(String candidate) {
        this.candidate = candidate;
    }

    @Enumerated(EnumType.ORDINAL)
    public CandidateParty getParty() {
        return party;
    }

    public void setParty(CandidateParty party) {
        this.party = party;
    }

    public int getVoteTotal() {
        return voteTotal;
    }

    public void setVoteTotal(int voteTotal) {
        this.voteTotal = voteTotal;
    }

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "precinct_uid")
    @JsonBackReference
    public Precinct getPrecinct() {
        return precinct;
    }

    public void setPrecinct(Precinct precinct) {
        this.precinct = precinct;
    }

    @Override
    public String toString() {
        return "ElectionData{" +
                "id=" + id +
                ", year=" + year +
                ", type=" + type +
                ", candidate='" + candidate + '\'' +
                ", party=" + party +
                ", voteTotal=" + voteTotal +
                '}';
    }
}