package edu.stonybrook.cs.GerryMander.Controller;

import edu.stonybrook.cs.GerryMander.Model.*;
import edu.stonybrook.cs.GerryMander.Model.Enum.StatePostalCode;
import edu.stonybrook.cs.GerryMander.Model.Error;
import edu.stonybrook.cs.GerryMander.Service.DataService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;


@RestController
@RequestMapping("/data")
public class DataController {

    private static final Logger logger = LoggerFactory.getLogger(DataController.class);

    @Autowired
    private DataService dataService;

    @GetMapping("/getprecinctsbycong")
    public ResponseEntity<List<Precinct>> getPrecinctsByCong(@RequestParam long congressionalID){
        HttpStatus status = HttpStatus.OK;
        List<Precinct> result = dataService.getPrecinctsByCong(congressionalID);
        if (result.size() < 1){
            status = HttpStatus.NOT_FOUND;
            logger.error("getPrecinctsByCong: result size is 0.");
        }

        return new ResponseEntity<>(result, status);
    }

    @GetMapping("/getcongbystate")
    public ResponseEntity<List<CongressionalDistrict>> getCongByState(@RequestParam StatePostalCode state){
        HttpStatus status = HttpStatus.OK;
        List<CongressionalDistrict> result = dataService.getCongByState(state);
        if (result.size() < 1){
            status = HttpStatus.NOT_FOUND;
            logger.error("getCongByState: result size is 0.");
        }

        return new ResponseEntity<>(result, status);
    }

    @GetMapping("/getstate")
    public ResponseEntity<State> getState(@RequestParam StatePostalCode state){
        HttpStatus status = HttpStatus.OK;
        State result = dataService.getState(state);
        if (result == null){
            status = HttpStatus.INTERNAL_SERVER_ERROR;
            logger.error("getState: result is null.");
        }

        return new ResponseEntity<>(result, status);
    }

    @GetMapping("/getstates")
    public ResponseEntity<List<State>> getStates(){
        HttpStatus status = HttpStatus.OK;
        List<State> result = dataService.getStates();
        if (result.size() < 1){
            status = HttpStatus.NOT_FOUND;
            logger.error("getStates: result is null.");
        }

        return new ResponseEntity<>(result, status);
    }

    @GetMapping("/getelectiondata")
    public ResponseEntity<List<ElectionData>> getElectionData(@RequestParam String uid) {
        HttpStatus status = HttpStatus.OK;
        List<ElectionData> result = dataService.getElectionData(uid);
        if (result.size() < 1) {
            status = HttpStatus.NOT_FOUND;
            logger.error("no election data");
        }
        return new ResponseEntity<>(result, status);
    }

    @GetMapping("/geterrors")
    public ResponseEntity<List<Error>> getErrors(@RequestParam StatePostalCode state){
        HttpStatus status = HttpStatus.OK;
        List<Error> result = dataService.getErrors(state);
        if (result.size() < 1){
            status = HttpStatus.NOT_FOUND;
            logger.error("getErrors: result size is 0.");
        }
        return new ResponseEntity<>(result, status);
    }

    @GetMapping("/getcorrectionlog")
    public ResponseEntity<List<Correction>> getCorrectionLog(){
        HttpStatus status = HttpStatus.OK;
        List<Correction> result = dataService.getCorrectionLog();
        if (result.size() < 1){
            status = HttpStatus.NOT_FOUND;
            logger.error("getCorrectionLog: result size is 0.");
        }
        return new ResponseEntity<>(result, status);
    }

    @GetMapping(value = "/getnationalparksdata", produces = "application/zip")
    public byte[] getNationalParksData() {
        return DataService.nationalParksData;
    }
}
