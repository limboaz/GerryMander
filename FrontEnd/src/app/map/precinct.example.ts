import * as l from 'leaflet';
import union from '@turf/union';

export const precinctStyle = {
  color: '#3b7693',
  weight: 2,
  opacity: 1.00
};

export const ghostStyle = {
  color: '#000000',
  weight: 2,
  fillOpacity: 0
};

export const errorStyle = {
  color: '#3b7693',
  fillColor: '#932f38',
  weight: 2,
  fillOpacity: 0.65
};

export const selectedStyle = {
  color: '#569335',
  weight: 2,
  opacity: 1.00
};

const highlightStyle = {
  color: '#dab037',
  weight: 2,
  opacity: 1.00
};

export class PrecinctExample {
  missingNeighbor: PrecinctExample;

  constructor(layerGeoJson) {
    this.feature = layerGeoJson;
    if (!layerGeoJson.properties.hasError) {
      this.layer = l.geoJSON(layerGeoJson, {style: precinctStyle});
    } else {
      this.error = layerGeoJson.properties.error.type;
      switch (layerGeoJson.properties.error.type) {
        case 'GHOST':
          this.layer = l.geoJSON(layerGeoJson, {style: ghostStyle});
          break;
        default:
          this.layer = l.geoJSON(layerGeoJson, {style: errorStyle});
      }
    }
    this.layer.wrapperPrecinct = this;
  }

  public neighbors: PrecinctExample[];
  public layer: l.Layer;
  public highlighted = false;
  public feature;
  public error;

  static joinPrecincts(precinct1: PrecinctExample, precinct2: PrecinctExample) {
    if (!(precinct1.error === 'GHOST' || precinct2.error === 'GHOST')
      && (!precinct1.neighbors.includes(precinct2) || !precinct2.neighbors.includes(precinct1))) {
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

  resetNeighbors(): void {
    for (const n of this.neighbors) {
      n.layer.resetStyle();
    }
    this.highlighted = false;
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
