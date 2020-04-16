package edu.stonybrook.cs.GerryMander.Controller;

import edu.stonybrook.cs.GerryMander.Service.BoundaryCorrectionService;
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
@RequestMapping("/boundarycorrection")
public class BoundaryCorrectionController {

    private static final Logger logger = LoggerFactory.getLogger(BoundaryCorrectionController.class);

    @Autowired
    private BoundaryCorrectionService boundaryCorrectionService;

    @PostMapping("/mergeprecincts")
    public ResponseEntity<String> mergePrecincts(@RequestBody Map<String, String> req){
        HttpStatus status = HttpStatus.OK;

        Integer errID = Integer.valueOf(req.get("errID"));
        String precinctA = req.get("precinctA");
        String precinctB = req.get("precinctB");

        String result = boundaryCorrectionService.mergePrecincts(errID, precinctA, precinctB);
        if(result == null){
            status = HttpStatus.INTERNAL_SERVER_ERROR;
            logger.error("mergePrecincts: return value is null. ");
        }
        return new ResponseEntity<>(result, status);
    }

    @PostMapping("/updateprecinctboundary")
    public ResponseEntity<Object> updatePrecinctBoundary(@RequestBody Map<String, String> req){
        HttpStatus status = HttpStatus.OK;

        Integer errID = Integer.valueOf(req.get("errID"));
        String uid = req.get("uid");
        String newBoundary = req.get("newBoundary");

        boundaryCorrectionService.updatePrecinctBoundary(errID, uid, newBoundary);

        return new ResponseEntity<>(status);
    }

    @PostMapping("/defineghostprecinct")
    public ResponseEntity<String> defineGhostPrecinct(@RequestBody Map<String, String> req){
        HttpStatus status = HttpStatus.OK;

        Integer errID = Integer.valueOf(req.get("errID"));
        String boundary = req.get("boundary");

        String result = boundaryCorrectionService.defineGhostPrecinct(errID, boundary);
        if(result == null){
            status = HttpStatus.INTERNAL_SERVER_ERROR;
            logger.error("defineGhostPrecinct: return value is null. ");
        }

        return new ResponseEntity<>(result, status);
    }
}
