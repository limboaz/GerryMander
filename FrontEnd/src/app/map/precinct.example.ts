import * as l from 'leaflet';
import * as exampleJSON from '../../assets/example.json';

export const precinctStyle = {
  color: '#3b7693',
  weight: 1,
  opacity: 1.00
};

const highlightStyle = {
  color: '#da0023',
  weight: 1,
  opacity: 1.00
};

export class PrecinctExample {
  public neighbors: PrecinctExample[];
  public layer: l.Layer;
  public highlighted = false;

  constructor(layerGeoJson) {
    this.layer = l.geoJSON(layerGeoJson, {style: precinctStyle});
    this.layer.wrapperPrecinct = this;
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

  addNeighbor(n: PrecinctExample) {
    this.neighbors.push(n);
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
// comment
export const exampleLayerGroup = l.layerGroup(examplePrecincts.map(e => e.layer));
