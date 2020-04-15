import {Injectable} from '@angular/core';
import {BehaviorSubject} from 'rxjs';
import * as l from 'leaflet';
import * as exampleJSON from '../assets/az_example.json';
import {PrecinctExample} from './map/precinct.example';


@Injectable({
  providedIn: 'root'
})
export class MapService {
  public mapSource = new BehaviorSubject(undefined);
  public currentMap = this.mapSource.asObservable();
  public exampleLayerGroup;
  public errors;

  constructor() {
    const examplePrecincts = (exampleJSON as any).features
      .map(e => new PrecinctExample(e));

    for (const example of examplePrecincts) {
      example.neighbors = examplePrecincts.filter(e => {
        const i = examplePrecincts.indexOf(example);
        return (exampleJSON as any).features[i].properties.neighbors.includes(examplePrecincts.indexOf(e));
      });
    }

    this.exampleLayerGroup = l.layerGroup(examplePrecincts.map(e => e.layer));
    this.errors = examplePrecincts.filter(e => e.feature.properties.hasError).map(e => {
      if (e.feature.properties.error.type  === 'MISSING') {
        e.missingNeighbor = examplePrecincts[e.feature.properties.error.missingNum];
      }
      return e;
    });
  }

  init() {
    const tiles = l.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
      minZoom: 5
    });

    const map = l.map('map', {
      center: [39.8282, -98.5795],
      zoom: 5,
      zoomControl: false
    });
    this.mapSource.next(map);
    tiles.addTo(map);
  }
}
