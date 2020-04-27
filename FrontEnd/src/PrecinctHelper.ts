import {Precinct} from './models/models';
import {highlightStyle} from './app/styles';

function getNeighbors(precinct: Precinct, currentPrecincts): Precinct[] {
  if (!precinct.neighbors) {
    return [];
  }
  return precinct.neighbors.map(p =>
    p.precinct1 === precinct.uid ? currentPrecincts[p.precinct2] : currentPrecincts[p.precinct1]);
}

export function highlightNeighbors(precinct: Precinct, currentPrecincts) {
  if (!precinct.highlighted) {
    for (const n of getNeighbors(precinct, currentPrecincts)) {
      n.layer.setStyle(highlightStyle);
    }
    precinct.highlighted = true;
  }
}

export function resetNeighbors(precinct: Precinct, currentPrecincts) {
  for (const n of getNeighbors(precinct, currentPrecincts)) {
    n.layer.resetStyle();
  }
  precinct.highlighted = false;
}

export function addNeighbor(precinct: Precinct, newNeighbor: Precinct) {
  // Add newNeighbor as neighbor to Precinct and vice versa
}

export function mergePrecincts(precinctA: Precinct, precinctB: Precinct): Precinct {
  return undefined;
}
