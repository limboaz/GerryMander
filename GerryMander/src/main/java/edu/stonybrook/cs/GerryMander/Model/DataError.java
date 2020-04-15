package edu.stonybrook.cs.GerryMander.Model;

import javax.persistence.Entity;
import java.util.Set;

@Entity
public class DataError extends Error{
    private float errorValue;

    public float getErrorValue() {
        return errorValue;
    }

    public void setErrorValue(float errorValue) {
        this.errorValue = errorValue;
    }
}
