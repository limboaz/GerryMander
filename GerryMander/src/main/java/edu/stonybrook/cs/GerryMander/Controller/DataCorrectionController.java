package edu.stonybrook.cs.GerryMander.Controller;


import edu.stonybrook.cs.GerryMander.Model.ElectionData;
import edu.stonybrook.cs.GerryMander.Model.PopulationData;
import edu.stonybrook.cs.GerryMander.Service.DataCorrectionService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

/*
 * Last edit: Yinuo
 * Date: April 15, 2020
 */

@RestController
@RequestMapping("/datacorrection")
public class DataCorrectionController {

    private static final Logger logger = LoggerFactory.getLogger(DataCorrectionController.class);

    @Autowired
    private DataCorrectionService dataCorrectionService;

    @PostMapping("/editelectiondata")
    public ResponseEntity<Object> editElectionData(@RequestParam Map<String, String> req){
        HttpStatus status = HttpStatus.OK;

        Integer errID = Integer.valueOf(req.get("errID"));
        String uid = req.get("uid");

        /* TODO: write marshallers/unmarshallers to convert JSON to corresponding objects.
            We can use Jackson 2, with its annotation.
            Leaving this as dummy value for now, will complete later.
         */

        dataCorrectionService.editElectionData(errID, uid, new ElectionData());

        return new ResponseEntity<>(status);
    }

    @PostMapping("/editpopulationdata")
    public ResponseEntity<Object> editPopulationData(@RequestParam Map<String, String> req){
        HttpStatus status = HttpStatus.OK;

        Integer errID = Integer.valueOf(req.get("errID"));
        String uid = req.get("uid");

        dataCorrectionService.editPopulationData(errID, uid, new PopulationData());

        return new ResponseEntity<>(status);
    }

    @PostMapping("/deleteneighbor")
    public ResponseEntity<Object> deleteNeighbor(@RequestBody Map<String,String> req){
        HttpStatus status = HttpStatus.OK;

        String uid = req.get("uid");
        String neighborID = req.get("neighborID");

        logger.info("params: uid = " + uid + ", neighborID = " + neighborID);

        dataCorrectionService.deleteNeighbor(uid, neighborID);

        return new ResponseEntity<>(status);
    }

    @PostMapping("/addneighbor")
    public ResponseEntity<Object> addNeighbor(@RequestBody Map<String, String> req){
        HttpStatus status = HttpStatus.OK;

        String uid = req.get("uid");
        String neighborID = req.get("neighborID");

        dataCorrectionService.addNeighbor(uid, neighborID);

        return new ResponseEntity<>(status);
    }

}
