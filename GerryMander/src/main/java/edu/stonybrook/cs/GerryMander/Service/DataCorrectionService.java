package edu.stonybrook.cs.GerryMander.Service;


import edu.stonybrook.cs.GerryMander.Model.*;
import edu.stonybrook.cs.GerryMander.Model.Enum.CorrectionType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import java.sql.Date;
import java.util.List;


@Service
public class DataCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(DataCorrectionService.class);

    @PersistenceContext
    EntityManager em;

    /*
     * if there's an error, we can throw an exception. Exception handling can happen later in
     * the implementation stage, as we want to see what's going on with db and figure out what
     * exceptions we need to handle. The controller will return different status code with
     * different exceptions.
     */

    public void editElectionData(Long errID, String uid, List<ElectionData> electionData){
        logger.info("editElectionData: errorID = " + errID + ", uid = " + uid);
        DataError err = em.find(DataError.class, errID);
        if(err != null){
            try{
                for(ElectionData item: electionData)
                    em.merge(item);
                err.setResolved(true);
                em.merge(err);

                Correction correction = new Correction();
                correction.setComment("Edited election data with id " + uid + ", errID " + errID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setAssociatedError(err);
                correction.setType(CorrectionType.ELECTION_DATA);
                em.persist(correction);
            }catch (Exception e){
                e.printStackTrace();
            }
        }else{
            logger.error("editElectionData: errorID = " + errID + ", uid = " + uid + ", error doesn't exist in database.");
        }
    }

    public void editPopulationData(Long errID, String uid, PopulationData populationData){
        logger.info("editPopulationData: errID = " + errID + ", uid = " + uid);
        DataError err = em.find(DataError.class, errID);
        if(err != null){
            try{
                em.merge(populationData);
                err.setResolved(true);
                em.merge(err);

                Correction correction = new Correction();
                correction.setComment("Edited population data with id " + uid + ", errID " + errID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setAssociatedError(err);
                correction.setType(CorrectionType.POPULATION_DATA);
                em.persist(correction);
            }catch (Exception e){
                e.printStackTrace();
            }
        }else{
            logger.error("editPopulationData: errorID = " + errID + ", uid = " + uid + ", error doesn't exist in database.");
        }
    }

    public void deleteNeighbor(String uid, String neighborID){
        logger.info("deleteNeighbor: uid = " + uid + ", neighborID = " + neighborID);
        Precinct precinct = em.find(Precinct.class, uid);
        if(precinct != null) {
            try{
                NeighborData neighbor = em.find(NeighborData.class, neighborID);
                precinct.getNeighbors().remove(neighbor);
                em.merge(precinct);
                em.remove(neighbor);

                Correction correction = new Correction();
                correction.setComment("Deleted neighbor data with id " + neighborID + ", uid = " + uid);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setType(CorrectionType.NEIGHBOR_CHANGE);
                em.persist(correction);
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        else{
            logger.error("deleteNeighbor: uid = " + uid + ", precinct doesn't exist in database.");
        }
    }

    public void addNeighbor(String uid, String neighborID){
        logger.info("addNeighbor: uid = " + uid + ", neighborID" + neighborID);
        Precinct precinct = em.find(Precinct.class, uid);
        if(precinct != null){
            try{
                NeighborData neighborData = new NeighborData(precinct, neighborID);
                em.persist(neighborData);
                precinct.getNeighbors().add(neighborData);
                em.merge(precinct);

                Correction correction = new Correction();
                correction.setComment("Added neighbor data with id " + neighborID + ", uid = " + uid);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setType(CorrectionType.NEIGHBOR_CHANGE);
                em.persist(correction);
            }catch(Exception e){
                e.printStackTrace();
            }
        }else{
            logger.error("addNeighbor: uid = " + uid + ", precinct doesn't exist in database.");
        }
    }
}
