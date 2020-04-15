package edu.stonybrook.cs.GerryMander.Model;

import edu.stonybrook.cs.GerryMander.Model.Enum.CorrectionType;

import java.util.Date;

public class Correction {
    int id;
    CorrectionType type;
    Date time;
    String comment;
    String oldValue;
    String newValue;
    Error associatedError;
}
