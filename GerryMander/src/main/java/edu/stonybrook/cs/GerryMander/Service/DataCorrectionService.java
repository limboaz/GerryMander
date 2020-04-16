package edu.stonybrook.cs.GerryMander.Service;


import edu.stonybrook.cs.GerryMander.Model.ElectionData;
import edu.stonybrook.cs.GerryMander.Model.PopulationData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

/*
 * Last edit: Yinuo
 * Date: April 15, 2020
 */

@Service
public class DataCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(DataCorrectionService.class);

    /*
     * if there's an error, we can throw an exception. Exception handling can happen later in
     * the implementation stage, as we want to see what's going on with db and figure out what
     * exceptions we need to handle. The controller will return different status code with
     * different exceptions.
     */

    public void editElectionData(Long errID, String uid, ElectionData electionData){
        logger.info("editElectionData: errorID = " + errID + ", uid = " + uid);
    }

    public void editPopulationData(Long errID, String uid, PopulationData populationData){
        logger.info("editPopulationData: errID = " + errID + ", uid = " + uid);
    }

    public void deleteNeighbor(String uid, String neighborID){
        logger.info("deleteNeighbor: uid = " + uid + ", neighborID = " + neighborID);
    }

    public void addNeighbor(String uid, String neighborID){
        logger.info("addNeighbor: uid = " + uid + ", neighborID" + neighborID);
    }
}
