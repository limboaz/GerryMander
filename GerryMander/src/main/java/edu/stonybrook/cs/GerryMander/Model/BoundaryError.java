package edu.stonybrook.cs.GerryMander.Model;

import javax.persistence.Entity;
import javax.persistence.Lob;
import javax.persistence.OneToMany;
import javax.persistence.Table;
import java.util.HashSet;

@Entity
public class BoundaryError extends Error {
    private String errorBoundaryGeoJSON;

    @Lob
    public String getErrorBoundaryGeoJSON() {
        return errorBoundaryGeoJSON;
    }

    public void setErrorBoundaryGeoJSON(String errorBoundaryGeoJSON) {
        this.errorBoundaryGeoJSON = errorBoundaryGeoJSON;
    }

}
