package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.CandidateParty;
import edu.stonybrook.cs.GerryMander.Model.Enum.ElectionType;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.Id;

@Entity
//TODO: add table name annotation
public class ElectionData {
    int id;
    int year;
    ElectionType type;
    String candidate;
    CandidateParty party;
    int voteTotal;

    @Id
    @GeneratedValue
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

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
}
