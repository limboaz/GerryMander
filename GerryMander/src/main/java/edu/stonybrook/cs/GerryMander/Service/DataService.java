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
import java.util.ArrayList;
import java.util.List;

/*
 * Last edit: Yinuo
 * Date: April 15, 2020
 */

@Service
public class DataService {

//    @PersistenceContext
//    private EntityManager em;

    private static Logger logger = LoggerFactory.getLogger(DataService.class);

    /*
     * NOTE: only dummy return values right now.
     */

    public List<Precinct> getPrecinctsByCong(String congressionalID){
        logger.info("getPrecinctsByCong: congressional = " + congressionalID);

        return new ArrayList<Precinct>();
    }

    public List<CongressionalDistrict> getCongByState(StatePostalCode state){
        logger.info("getCongByState: state = " + state.name());

        return new ArrayList<CongressionalDistrict>();
    }

    public State getState(StatePostalCode state){
        logger.info("getState: state = " + state.name());

        return new State();
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
