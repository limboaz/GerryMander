import {NeighborData, Precinct} from './models/models';
import {highlightStyle} from './app/styles';
import {stringify} from 'querystring';

export const warningMessage = 'Please select the corresponding error this will fix first and try again';
export const notificationType = 'warning';

function getNeighbors(precinct: Precinct, currentPrecincts): Precinct[] {
  if (!precinct.neighbors) {
    return [];
  }
  const neighbors = precinct.neighbors.map(p => currentPrecincts[p.neighborID]).filter(p => p !== undefined);
  return neighbors;
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

export function addNeighbor(http, precinct: Precinct, newNeighbor: Precinct, currentPrecincts) {
  loadRequest(http.post('/datacorrection/addneighbor', {uid: precinct.uid, neighborID: newNeighbor.uid}, {responseType: 'text'}),
    (id) => {
      precinct.neighbors.push({id, neighborID: newNeighbor.uid});
      highlightNeighbors(precinct, currentPrecincts);
    });
}

export function removeNeighbor(http, precinct: Precinct, oldNeighbor: Precinct, currentPrecincts) {
  if (!getNeighbors(precinct, currentPrecincts).includes(oldNeighbor)) {
    return false;
  }
  let neighborID;
  for (const n of precinct.neighbors) {
    if (n.neighborID === oldNeighbor.uid) { neighborID = n.id; }
  }
  loadRequest(http.post('/datacorrection/deleteneighbor', {uid: precinct.uid, neighborID}),
    () => {
      resetNeighbors(precinct, currentPrecincts);
      precinct.neighbors = precinct.neighbors.filter(p => p.neighborID !== oldNeighbor.uid);
      highlightNeighbors(precinct, currentPrecincts);
    });
  return true;
}

export function updateBoundary(http, precinct: Precinct, newBoundary, errID) {
  newBoundary = JSON.stringify(newBoundary.features[0].geometry);
  loadRequest(http.post('/boundarycorrection/updateprecinctboundary', {uid: precinct.uid, errID, newBoundary}),
    () => console.log('I finished updating'));
}

export function loadRequest(httpRequest, successCallback) {
  const leafletStyle = document.getElementById('leafletStyle');
  leafletStyle.innerHTML = '';
  leafletStyle.appendChild(document.createTextNode('.leaflet-interactive, #map { cursor: wait !important; }'));
  httpRequest.subscribe(d => {
    leafletStyle.innerHTML = '';
    leafletStyle.appendChild(document.createTextNode('.leaflet-interactive, #map { cursor: auto; }'));
    successCallback(d);
  }, (e) => {
    console.log(e);
    leafletStyle.innerHTML = '';
    leafletStyle.appendChild(document.createTextNode('.leaflet-interactive, #map { cursor: auto; }'));
  });
}
