package edu.stonybrook.cs.GerryMander.Service;

import edu.stonybrook.cs.GerryMander.Model.CongressionalDistrict;
import edu.stonybrook.cs.GerryMander.Model.Error;
import edu.stonybrook.cs.GerryMander.Model.Correction;
import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;
import edu.stonybrook.cs.GerryMander.Model.Precinct;
import edu.stonybrook.cs.GerryMander.Model.State;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.ArrayList;
import java.util.List;


@Service
public class DataService {

    @PersistenceContext
    private EntityManager em;

    private static Logger logger = LoggerFactory.getLogger(DataService.class);

    public List<Precinct> getPrecinctsByCong(long congressionalID){
        logger.info("getPrecinctsByCong: congressional = " + congressionalID);
        Query query = em.createQuery("from Precinct P where P.congDistrictNum = " + congressionalID);
        return (List<Precinct>)query.getResultList();
    }

    public List<CongressionalDistrict> getCongByState(StatePostalCode state){
        logger.info("getCongByState: state = " + state.name());
        Query query = em.createQuery("from CongressionalDistrict CD where CD.stateCode = " + state.ordinal());
        return (List<CongressionalDistrict>)query.getResultList();
    }

    public State getState(StatePostalCode state){
        logger.info("getState: state = " + state.name());

        return em.find(State.class, state);
    }

    public List<Error> getErrors(StatePostalCode state){
        logger.info("getErrors: state = " + state.name());
        return new ArrayList<Error>();
    }

    public List<Correction> getCorrectionLog() {
        logger.info("getCorrectionLog: called. ");
        return new ArrayList<Correction>();
    }
}
