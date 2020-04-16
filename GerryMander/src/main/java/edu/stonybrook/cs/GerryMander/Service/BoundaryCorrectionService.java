package edu.stonybrook.cs.GerryMander.Service;

import edu.stonybrook.cs.GerryMander.Model.Correction;
import edu.stonybrook.cs.GerryMander.Model.Precinct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;



@Service
public class BoundaryCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(BoundaryCorrectionService.class);

    public String mergePrecincts(Long errID, String precinctA, String precinctB){
        logger.info("mergePrecincts: errID = " + errID + ", precinctA = " + precinctA + ", precinctB = " + precinctB);

        return "mergePrecincts is called.";
    }

    public void updatePrecinctBoundary(Long errID, String uid, String newBoundary){
        logger.info("updatePrecinctBoundary: errID = " + errID + ", uid = " + uid);
    }

    public String defineGhostPrecinct(Long errID, String boundary, String precinctID){
        logger.info("defineGhostPrecinct: errID = " + errID);

        Precinct precinct = new Precinct(precinctID);
        precinct.setPrecinctGeoJSON(boundary);

        //TODO: persist ghost precinct

        Correction correction = new Correction();

        return "defineGhostPrecinct is called.";
    }

    private void checkBoundaries(Precinct precinct){

    }

    // Considering that we are using JPA, is this still necessary?
    private void deletePrecinct(Precinct precinct){

    }
}
