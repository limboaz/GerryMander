package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import edu.stonybrook.cs.GerryMander.Model.Enum.CandidateParty;
import edu.stonybrook.cs.GerryMander.Model.Enum.ElectionType;

import javax.persistence.*;
import java.util.*;

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

    public ElectionData(){}

    public ElectionData(int year, ElectionType type, String candidate, CandidateParty party, int voteTotal, Precinct precinct){
        this.year = year;
        this.type = type;
        this.candidate = candidate;
        this.party = party;
        this.voteTotal = voteTotal;
        this.precinct = precinct;
    }

    public static List<ElectionData> mergeElection(List<ElectionData> electA, List<ElectionData> electB){
        Map<String, ElectionData> mergedElection = new HashMap<>();
        for(ElectionData item: electA)
            mergedElection.put(item.getYear() + item.getCandidate(), item);
        for(ElectionData item: electB){
            if(mergedElection.containsKey(item.getYear() + item.getCandidate())){
                ElectionData prev = mergedElection.get(item.getYear() + item.getCandidate());
                mergedElection.put(item.getYear() + item.getCandidate(), new ElectionData(item.getYear(), item.getType(), item.getCandidate(), item.getParty(), item.getVoteTotal() + prev.getVoteTotal(), item.getPrecinct()));
            }else{
                mergedElection.put(item.getYear() + item.getCandidate(), item);
            }
        }
        return new ArrayList<>(mergedElection.values());
    }

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