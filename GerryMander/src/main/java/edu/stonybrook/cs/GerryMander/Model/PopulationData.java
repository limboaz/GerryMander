package edu.stonybrook.cs.GerryMander.Model;

import com.fasterxml.jackson.annotation.JsonBackReference;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

import javax.persistence.*;


@Entity
@JsonIgnoreProperties("precinct")
public class PopulationData {
    private String id;
    private int total;
    private int white;
    private int black;
    private int asian;
    private int hispanic;
    private int nativeAmerican;
    private int pacificIslander;
    private int other;
    private Precinct precinct;

    public PopulationData(){}

    public PopulationData(String id, int total, int white, int black, int asian, int hispanic, int nativeAmerican,
                          int pacificIslander, int other, Precinct precinct){
        this.id = id;
        this.total = total;
        this.white = white;
        this.black = black;
        this.asian = asian;
        this.hispanic = hispanic;
        this.nativeAmerican = nativeAmerican;
        this.pacificIslander = pacificIslander;
        this.other = other;
        this.precinct = precinct;
    }

    static public PopulationData mergePop(Precinct precinctA, Precinct precinctB, Precinct mergedPrecinct){
        PopulationData popA = precinctA.getPopulationData();
        PopulationData popB = precinctB.getPopulationData();

        if (popA == null && popB == null) {
            PopulationData newPop = new PopulationData();
            newPop.setId(mergedPrecinct.getUid() + "_POP_" + 0);
            return newPop;
        } else if (popA == null) {
            return new PopulationData(mergedPrecinct.getUid() + "_POP_" + popB.getTotal(), popB.getTotal(), popB.getWhite(), popB.getBlack(),
                    popB.getAsian(), popB.getHispanic(), popB.getNativeAmerican(), popB.getPacificIslander(), popB.getOther(), mergedPrecinct);
        } else if (popB == null) {
            return new PopulationData(mergedPrecinct.getUid() + "_POP_" + popA.getTotal(), popA.getTotal(), popA.getWhite(), popA.getBlack(),
                    popA.getAsian(), popA.getHispanic(), popA.getNativeAmerican(), popA.getPacificIslander(), popA.getOther(), mergedPrecinct);
        }
        return new PopulationData(mergedPrecinct.getUid() + "_POP_" + popA.getTotal(), popA.getTotal() + popB.getTotal(), popA.getWhite() + popB.getWhite(), popA.getBlack() + popB.getBlack(),
                popA.getAsian() + popB.getAsian(), + popA.getHispanic() + popB.getHispanic(), + popA.getNativeAmerican() + popB.getNativeAmerican(),
                popA.getPacificIslander() + popB.getPacificIslander(), popA.getOther() + popB.getOther(), mergedPrecinct);
    }

    @Id
    @Column(length = 100)
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }

    public int getWhite() {
        return white;
    }

    public void setWhite(int white) {
        this.white = white;
    }

    public int getBlack() {
        return black;
    }

    public void setBlack(int black) {
        this.black = black;
    }

    public int getAsian() {
        return asian;
    }

    public void setAsian(int asian) {
        this.asian = asian;
    }

    public int getHispanic() {
        return hispanic;
    }

    public void setHispanic(int hispanic) {
        this.hispanic = hispanic;
    }

    public int getNativeAmerican() {
        return nativeAmerican;
    }

    public void setNativeAmerican(int nativeAmerican) {
        this.nativeAmerican = nativeAmerican;
    }

    public int getPacificIslander() {
        return pacificIslander;
    }

    public void setPacificIslander(int pacificIslander) {
        this.pacificIslander = pacificIslander;
    }

    public int getOther() {
        return other;
    }

    public void setOther(int other) {
        this.other = other;
    }

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "precinct_uid")
    @JsonBackReference
    public Precinct getPrecinct() {
        return precinct;
    }

    public void setPrecinct(Precinct precinct) {
        this.precinct = precinct;
    }
}