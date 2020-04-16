package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.CandidateParty;
import edu.stonybrook.cs.GerryMander.Model.Enum.ElectionType;

import javax.persistence.*;

@Entity
//TODO: add table name annotation
public class ElectionData {
    private long id;
    private int year;
    private ElectionType type;
    private String candidate;
    private CandidateParty party;
    private int voteTotal;

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
