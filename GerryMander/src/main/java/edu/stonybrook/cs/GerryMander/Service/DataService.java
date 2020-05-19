package edu.stonybrook.cs.GerryMander.Service;

import edu.stonybrook.cs.GerryMander.Model.*;
import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;
import edu.stonybrook.cs.GerryMander.Model.Error;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


@Service
public class DataService {

    public static byte[] nationalParksData;

    static {
        try {
            nationalParksData = new FileInputStream("nps_boundary.zip").readAllBytes();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @PersistenceContext
    private EntityManager em;

    private static Logger logger = LoggerFactory.getLogger(DataService.class);

    public List<Precinct> getPrecinctsByCong(long congressionalID){
        logger.info("getPrecinctsByCong: congressional = " + congressionalID);
        CongressionalDistrict cd = em.find(CongressionalDistrict.class, congressionalID);
        if (cd.getPrecincts() == null) {
            return List.of();
        }

        for (Precinct p: cd.getPrecincts()) {
            p.setNeighbors(null);
            p.setElectionData(null);
        }
        return cd.getPrecincts();
    }

    public List<CongressionalDistrict> getCongByState(StatePostalCode state){
        logger.info("getCongByState: state = " + state.name());
        State s = em.find(State.class, state);
        for (CongressionalDistrict c: s.getCongressionalDistricts()) {
            c.setPrecincts(null);
        }
        return s.getCongressionalDistricts();
    }

    public State getState(StatePostalCode state){
        logger.info("getState: state = " + state.name());
        State s = em.find(State.class, state);
        s.setCongressionalDistricts(null);
        s.setErrors(null);
        return s;
    }

    public List<State> getStates(){
        logger.info("getStates");
        List<State> states = em.createQuery("select S from State as S").getResultList();
        for (State s: states) {
            s.setErrors(null);
            s.setCongressionalDistricts(null);
        }
        return states;
    }

    public List<Error> getErrors(StatePostalCode state){
        logger.info("getErrors: state = " + state.name());
        List<Error> errorsList = new ArrayList<>(em.find(State.class, state).getErrors());
        for (Error e: errorsList) {
            e.setCorrections(null);
        }
        return errorsList;
    }

    public List<Correction> getCorrectionLog() {
        logger.info("getCorrectionLog: called. ");
        return new ArrayList<Correction>(em.createQuery("select e from Correction e").getResultList());
    }

    public List<ElectionData> getElectionData(String uid) {
        logger.info("getPrecinctData: uid = " + uid);
        return em.find(Precinct.class, uid).getElectionData();
    }

    public List<NeighborData> getPrecinctNeighbors(String uid) {
        logger.info("getPrecinctNeighbors: uid = " + uid);
        return em.find(Precinct.class, uid).getNeighbors();
    }
}
