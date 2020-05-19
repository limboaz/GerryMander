package edu.stonybrook.cs.GerryMander.Service;

import edu.stonybrook.cs.GerryMander.Model.*;
import edu.stonybrook.cs.GerryMander.Model.Enum.CorrectionType;
import edu.stonybrook.cs.GerryMander.Model.Error;
import org.locationtech.jts.geom.Geometry;
import org.locationtech.jts.geom.GeometryCollection;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.io.ParseException;
import org.locationtech.jts.io.geojson.GeoJsonReader;
import org.locationtech.jts.io.geojson.GeoJsonWriter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManager;
import javax.persistence.FlushModeType;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import javax.transaction.Transactional;
import java.sql.Date;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;


@Service
public class BoundaryCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(BoundaryCorrectionService.class);

    @PersistenceContext
    private EntityManager em;

    @Transactional
    public Precinct mergePrecincts(Long errID, String precinctA, String precinctB){
        logger.info("mergePrecincts: errID = " + errID + ", precinctA = " + precinctA + ", precinctB = " + precinctB);

        Query query = em.createQuery("select P from Precinct as P where P.uid in (:ids)");
        query.setParameter("ids", List.of(precinctA, precinctB));
        List<Precinct> precincts = query.getResultList();
        Precinct preA = precincts.get(0);
        Precinct preB = precincts.get(1);
        em.setFlushMode(FlushModeType.COMMIT);

        if (query.getResultList().size() > 0) {
            GeoJsonReader reader = new GeoJsonReader();
            GeoJsonWriter writer = new GeoJsonWriter();
            try {
                Geometry aGeoJSON = reader.read(preA.getPrecinctGeoJSON());
                Geometry bGeoJSON = reader.read(preB.getPrecinctGeoJSON());
                GeometryCollection geometryCollection = new GeometryCollection(new Geometry[]{aGeoJSON, bGeoJSON}, new GeometryFactory());
                String mergedBoundary = writer.write(geometryCollection.union());

                Precinct mergedPrecinct = new Precinct();
                mergedPrecinct.setPrecinctGeoJSON(mergedBoundary);
                String uid = preA.getState().name() + "_" + preA.getCounty() + "_" + preA.getName() + preB.getName();
                uid = uid.replaceAll(" ", "_").toUpperCase();
                mergedPrecinct.setUid(uid);

                PopulationData mergedPop = PopulationData.mergePop(preA, preB, mergedPrecinct);
                mergedPrecinct.setPopulationData(mergedPop);

                mergedPrecinct.setState(preA.getState());
                mergedPrecinct.setCongDistrictNum(preA.getCongDistrictNum());
                mergedPrecinct.setCongressionalDistrict(preA.getCongressionalDistrict());
                mergedPrecinct.setName(preA.getName() + " + " + preB.getName());
                mergedPrecinct.setCounty(preA.getCounty());

                List<ElectionData> mergedElection = ElectionData.mergeElection(preA.getElectionData(), preB.getElectionData(), mergedPrecinct);
                mergedPrecinct.setElectionData(mergedElection);

                List<NeighborData> mergedNeighbor = NeighborData.mergeNeighbors(mergedPrecinct, preA.getNeighbors(), preB.getNeighbors());
                mergedPrecinct.setNeighbors(mergedNeighbor);

                BoundaryError err = em.find(BoundaryError.class, errID);
                err.setResolved(true);
                em.merge(err);

                Correction correction = new Correction();
                correction.setComment("Merged precincts with id " + precinctA + ", " + precinctB + ", errID " + errID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setOldValue("precinct A:" + precinctA + ", precinct B: " + precinctB);
                correction.setNewValue("New precinct:" + uid);
                correction.setAssociatedError(err);
                correction.setType(CorrectionType.MERGE_PRECINCT);
          
                em.persist(correction);
                em.persist(mergedPrecinct);

                preA.setPrecinctGeoJSON("{\"type\": \"Point\", \"coordinates\": [0.0, 0.0]}");
                preB.setPrecinctGeoJSON("{\"type\": \"Point\", \"coordinates\": [0.0, 0.0]}");
                em.merge(preA);
                em.merge(preB);
                return mergedPrecinct;
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }else{
            logger.error("mergePrecincts: errID = " + errID + ", precincts don't exist in database.");
        }
        return null;
    }


    @Transactional
    public void updatePrecinctBoundary(Long errID, String uid, String newBoundary){
        logger.info("updatePrecinctBoundary: errID = " + errID + ", uid = " + uid);
        Precinct precinct = em.find(Precinct.class, uid);
        if(precinct != null){
            try {
                String oldBoundary = precinct.getPrecinctGeoJSON();
                precinct.setPrecinctGeoJSON(newBoundary);
                em.merge(precinct);

                BoundaryError err = em.find(BoundaryError.class, errID);
                err.setResolved(true);
                em.merge(err);

                Correction correction = new Correction();
                correction.setComment("Updated precinct boundary " + uid + ", errID " + errID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setOldValue(oldBoundary);
                correction.setNewValue(newBoundary);
                correction.setAssociatedError(err);
                correction.setType(CorrectionType.BOUNDARY_CHANGE);
                em.persist(correction);
            }
            catch(Exception e){
                e.printStackTrace();
            }
        }else{
            logger.error("updatePrecinctBoundary: errID = " + errID + ", uid = " + uid + ", precinct doesn't exist in database.");
        }
    }

    @Transactional
    public String defineGhostPrecinct(Long errID){
        logger.info("defineGhostPrecinct: errID = " + errID);
        BoundaryError err = em.find(BoundaryError.class, errID);
        if(err != null){
            try {
                String uid = err.getState().getName() + "_" + err.getCongId() + "_" + errID;
                Precinct precinct = new Precinct(uid);
                precinct.setPrecinctGeoJSON(err.getErrorBoundaryGeoJSON());
                em.persist(precinct);

                err.setResolved(true);
                em.merge(err);

                Correction correction = new Correction();
                correction.setComment("Generating ghost precinct with id " + uid + ", errID " + errID);
                correction.setTime(new Date(System.currentTimeMillis()));
                correction.setNewValue(uid);
                correction.setAssociatedError(err);
                correction.setType(CorrectionType.GHOST_DESIGNATION);
                em.persist(correction);

                return uid;
            }catch(Exception e){
                e.printStackTrace();
            }
        }else{
            logger.error("defineGhostPrecinct: errID = " + errID + ", error doesn't exist in database.");
        }
        return null;
    }
}
