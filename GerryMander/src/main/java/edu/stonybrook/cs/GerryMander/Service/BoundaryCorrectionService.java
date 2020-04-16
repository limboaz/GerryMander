package edu.stonybrook.cs.GerryMander.Service;

import edu.stonybrook.cs.GerryMander.Model.Precinct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/*
 * Last edit: Yinuo
 * Date: April 15, 2020
 */

@Service
public class BoundaryCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(BoundaryCorrectionService.class);

    public String mergePrecincts(Integer errID, String precinctA, String precinctB){
        logger.info("mergePrecincts: errID = " + errID + ", precinctA = " + precinctA + ", precinctB = " + precinctB);

        return "mergePrecincts is called.";
    }

    public void updatePrecinctBoundary(Integer errID, String uid, String newBoundary){
        logger.info("updatePrecinctBoundary: errID = " + errID + ", uid = " + uid);
    }

    public String defineGhostPrecinct(Integer errID, String boundary){
        logger.info("defineGhostPrecinct: errID = " + errID);
        return "defineGhostPrecinct is called.";
    }

    private void checkBoundaries(Precinct precinct){

    }

    // Considering that we are using JPA, is this still necessary?
    private void deletePrecinct(Precinct precinct){

    }
}
