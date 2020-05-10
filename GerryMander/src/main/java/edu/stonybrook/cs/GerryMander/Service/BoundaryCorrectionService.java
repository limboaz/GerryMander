package edu.stonybrook.cs.GerryMander.Service;

import edu.stonybrook.cs.GerryMander.Model.Correction;
import edu.stonybrook.cs.GerryMander.Model.Precinct;
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
import javax.persistence.PersistenceContext;
import javax.persistence.Query;
import java.util.List;



@Service
public class BoundaryCorrectionService {

    private static final Logger logger = LoggerFactory.getLogger(BoundaryCorrectionService.class);

    @PersistenceContext
    private EntityManager em;

    public Precinct mergePrecincts(Long errID, String precinctA, String precinctB){
        logger.info("mergePrecincts: errID = " + errID + ", precinctA = " + precinctA + ", precinctB = " + precinctB);

        Query query = em.createQuery("select P from Precinct as P where P.uid in (:ids)");
        query.setParameter("ids", List.of(precinctA, precinctB));
        List<Precinct> precincts = query.getResultList();

        if (query.getResultList().size() > 0) {
            GeoJsonReader reader = new GeoJsonReader();
            GeoJsonWriter writer = new GeoJsonWriter();
            try {
                Geometry aGeoJSON = reader.read(precincts.get(0).getPrecinctGeoJSON());
                Geometry bGeoJSON = reader.read(precincts.get(1).getPrecinctGeoJSON());
                GeometryCollection geometryCollection = new GeometryCollection(new Geometry[]{aGeoJSON, bGeoJSON}, new GeometryFactory());
                String mergedBoundary = writer.write(geometryCollection.union());

                Precinct mergedPrecinct = new Precinct();

                mergedPrecinct.setPrecinctGeoJSON(mergedBoundary);
                return mergedPrecinct;
            } catch (ParseException e) {
                e.printStackTrace();
            }
        }
        return null;
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
