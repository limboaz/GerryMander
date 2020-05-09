import {Precinct} from './models/models';
import {highlightStyle} from './app/styles';

function getNeighbors(precinct: Precinct, currentPrecincts): Precinct[] {
  if (!precinct.neighbors) {
    return [];
  }
  return precinct.neighbors.map(p => currentPrecincts[p.neighborID]);
}

export function highlightNeighbors(precinct: Precinct, currentPrecincts) {
  for (const n of getNeighbors(precinct, currentPrecincts)) {
    n.layer.setStyle(highlightStyle);
  }
}

export function resetNeighbors(precinct: Precinct, currentPrecincts) {
  for (const n of getNeighbors(precinct, currentPrecincts)) {
    n.layer.resetStyle();
  }
}

export function addNeighbor(precinct: Precinct, newNeighbor: Precinct, currentPrecincts) {
  // Add newNeighbor as neighbor to Precinct and vice versa
  highlightNeighbors(precinct, currentPrecincts);
}

export function removeNeighbor(precinct: Precinct, oldNeighbor: Precinct, currentPrecincts) {
  // remove neighbor
}

export function mergePrecincts(precinctA: Precinct, precinctB: Precinct): Precinct {
  return undefined;
}
