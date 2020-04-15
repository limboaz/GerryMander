package edu.stonybrook.cs.GerryMander.Model;

import java.util.Set;

public class BoundaryError extends Error {
    String errorBoundaryGeoJSON;
    Set<String> precinctsAssoicated;
}
