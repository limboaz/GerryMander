import * as l from 'leaflet';
import * as exampleJSON from '../../assets/example.json';
import intersect from '@turf/intersect';
import union from '@turf/union';

export const precinctStyle = {
  color: '#3b7693',
  weight: 2,
  opacity: 1.00
};

const highlightStyle = {
  color: '#da0023',
  weight: 2,
  opacity: 1.00
};

export class PrecinctExample {

  constructor(layerGeoJson) {
    this.feature = layerGeoJson;
    this.layer = l.geoJSON(layerGeoJson, {style: precinctStyle});
    this.layer.wrapperPrecinct = this;
  }

  public neighbors: PrecinctExample[];
  public layer: l.Layer;
  public highlighted = false;
  public feature;

  static joinPrecincts(precinct1: PrecinctExample, precinct2: PrecinctExample) {
    if (!precinct1.neighbors.includes(precinct2) || !precinct2.neighbors.includes(precinct1)) {
      console.log('Cannot join precincts that are not neighbors');
      return undefined;
    }
    const combinedPrecincts = union(precinct1.feature, precinct2.feature);
    const newPrecinct = new PrecinctExample(combinedPrecincts);

    const unionNeighbors = precinct1.neighbors.filter(n => n !== precinct2);
    for (const n of precinct2.neighbors) {
      if (n !== precinct1 && !unionNeighbors.includes(n)) {
        unionNeighbors.push(n);
      }
    }
    for (const n of unionNeighbors) {
      n.neighbors.push(newPrecinct);
    }
    newPrecinct.neighbors = unionNeighbors;

    return newPrecinct;
  }

  highlightNeighbors(): void {
    if (!this.highlighted) {
      for (const n of this.neighbors) {
        n.layer.setStyle(highlightStyle);
      }
      this.highlighted = true;
    } else {
      for (const n of this.neighbors) {
        n.layer.resetStyle();
      }
      this.highlighted = false;
    }
  }

  addNeighbor(n: PrecinctExample): boolean {
    if (n !== this) {
      this.neighbors.push(n);
      return true;
    } else {
      console.log('Can\'t add as neighbor');
      return false;
    }
  }
}

const examplePrecincts = (exampleJSON as any).features
  .map(e => new PrecinctExample(e));

for (const example of examplePrecincts) {
  example.neighbors = examplePrecincts.filter(e => {
    const i = examplePrecincts.indexOf(example);
    return (exampleJSON as any).features[i].properties.neighbors.includes(examplePrecincts.indexOf(e));
  });
}

export const exampleLayerGroup = l.layerGroup(examplePrecincts.map(e => e.layer));
