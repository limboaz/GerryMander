package edu.stonybrook.cs.GerryMander.Service;


import edu.stonybrook.cs.GerryMander.Model.*;
import edu.stonybrook.cs.GerryMander.Model.Enum.CorrectionType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.transaction.Transactional;
import java.sql.Date;
import java.util.List;


@Service
public class DataCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(DataCorrectionService.class);

    @PersistenceContext
    EntityManager em;

    @Transactional
    public void editElectionData(Long errID, String uid, List<ElectionData> electionData){
        logger.info("editElectionData: errorID = " + errID + ", uid = " + uid);
        DataError err = em.find(DataError.class, errID);
        Precinct precinct = em.find(Precinct.class, uid);
        if(err != null){
            try{
                for(ElectionData item: electionData) {
                    item.setPrecinct(precinct);
                    logger.info("item: " + item.getPrecinct().getUid());
                    em.merge(item);
                }
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

    @Transactional
    public void editPopulationData(Long errID, String uid, PopulationData populationData){
        logger.info("editPopulationData: errID = " + errID + ", uid = " + uid);
        DataError err = em.find(DataError.class, errID);
        if(err != null){
            try{
                PopulationData oldPop = em.find(PopulationData.class, uid);
                Correction correction = new Correction();
                correction.setComment("Edited population data with id " + uid + ", errID " + errID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setOldValue(oldPop.toString());
                correction.setNewValue(populationData.toString());
                correction.setAssociatedError(err);
                correction.setType(CorrectionType.POPULATION_DATA);

                em.merge(populationData);
                err.setResolved(true);
                em.merge(err);
                em.persist(correction);
            }catch (Exception e){
                e.printStackTrace();
            }
        }else{
            logger.error("editPopulationData: errorID = " + errID + ", uid = " + uid + ", error doesn't exist in database.");
        }
    }

    @Transactional
    public void deleteNeighbor(String uid, String neighborID){
        logger.info("deleteNeighbor: uid = " + uid + ", neighborID = " + neighborID);
        Precinct precinct = em.find(Precinct.class, uid);
        if(precinct != null) {
            try{
                NeighborData neighbor = em.find(NeighborData.class, neighborID);
                //precinct.getNeighbors().remove(neighbor);

                Correction correction = new Correction();
                correction.setComment("Deleted neighbor data with id " + neighborID + ", uid = " + uid);
                correction.setOldValue(neighborID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setType(CorrectionType.NEIGHBOR_CHANGE);

                //em.merge(precinct);
                em.remove(neighbor);
                em.persist(correction);
            }catch(Exception e){
                e.printStackTrace();
            }
        }
        else{
            logger.error("deleteNeighbor: uid = " + uid + ", precinct doesn't exist in database.");
        }
    }

    @Transactional
    public String addNeighbor(String uid, String neighborID){
        logger.info("addNeighbor: uid = " + uid + ", neighborID" + neighborID);
        Precinct precinct = em.find(Precinct.class, uid);
        if(precinct != null){
            NeighborData neighborData = new NeighborData(precinct, neighborID);
            int seq = precinct.getNeighbors().size() + 1;
            String newNeighborID = precinct.getUid() + "_NEIGHBOR_" + seq;
            neighborData.setId(newNeighborID);
            precinct.getNeighbors().add(neighborData);
            em.persist(neighborData);
            em.merge(precinct);

            Correction correction = new Correction();
            correction.setComment("Added neighbor data with id " + neighborID + ", uid = " + uid);
            correction.setTime(new Date(System.currentTimeMillis()));
            correction.setType(CorrectionType.NEIGHBOR_CHANGE);
            correction.setNewValue(neighborID);
            em.persist(correction);

            return newNeighborID;
        }
        throw new IllegalArgumentException();
    }
}
