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
    private String id;
    private int year;
    private ElectionType type;
    private String candidate;
    private CandidateParty party;
    private int voteTotal;
    private Precinct precinct;

    public ElectionData(){}

    public ElectionData(String id, int year, ElectionType type, String candidate, CandidateParty party, int voteTotal, Precinct precinct){
        this.id = id;
        this.year = year;
        this.type = type;
        this.candidate = candidate;
        this.party = party;
        this.voteTotal = voteTotal;
        this.precinct = precinct;
    }

    public static List<ElectionData> mergeElection(List<ElectionData> electA, List<ElectionData> electB, Precinct precinct){
        int counter = 0;
        Map<String, ElectionData> mergedElection = new HashMap<>();
        for(ElectionData item: electA) {
            ElectionData newItem = new ElectionData(precinct.getUid() + "_ELECTION_" + counter, item.year, item.type, item.candidate,
                    item.party, item.voteTotal, precinct);
            counter++;
            mergedElection.put(newItem.getYear() + newItem.getCandidate(), newItem);
        }
        for(ElectionData item: electB){
            if(mergedElection.containsKey(item.getYear() + item.getCandidate())){
                ElectionData prev = mergedElection.get(item.getYear() + item.getCandidate());
                ElectionData newItem = new ElectionData(precinct.getUid() + "_ELECTION_" + counter, item.year, item.type, item.candidate,
                        item.party, item.voteTotal + prev.getVoteTotal(), precinct);
                mergedElection.put(item.getYear() + item.getCandidate(), newItem);
                counter++;
            }else{
                ElectionData newItem = new ElectionData(precinct.getUid() + "_ELECTION_" + counter, item.year, item.type, item.candidate,
                        item.party, item.voteTotal, precinct);
                counter++;
                mergedElection.put(newItem.getYear() + newItem.getCandidate(), newItem);
            }
        }
        return new ArrayList<>(mergedElection.values());
    }

    @Id
    @Column(length = 100)
    public String getId() {
        return id;
    }

    public void setId(String id) {
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