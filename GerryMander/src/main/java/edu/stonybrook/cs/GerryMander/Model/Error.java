package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.ErrorType;

public abstract class Error {
    int id;
    ErrorType type;
    String datasource;
}
