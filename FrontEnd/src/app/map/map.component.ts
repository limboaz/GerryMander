import {AfterViewInit, Component} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {forkJoin} from 'rxjs';

import * as l from 'leaflet';
import * as statesGeoJSON from '../../assets/us_states_500K.json';

const stateStyle = {
  color: '#ff7800',
  weight: 5,
  opacity: 0.65
};
const precinctStyle = {
  color: '#78eeff',
  weight: 1,
  opacity: 0.65
};
const districtStyle = {
  color: '#ff95f8',
  weight: 3,
  opacity: 0.65
};

const states = (statesGeoJSON as any).features
  .filter(e => ['WI', 'AZ', 'OH'].includes(e.properties.STUSPS))
  .map(e => {
    const s = l.geoJSON(e, {style: stateStyle});
    s.STUSPS = e.properties.STUSPS;
    s.NAME = e.properties.NAME;
    return s;
  });

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})

export class MapComponent implements AfterViewInit {
  private map;

  constructor(private http: HttpClient) {
  }

  ngAfterViewInit(): void {
    const az = this.http.get('assets/arizona.json');
    const wi = this.http.get('assets/wisconsin_wards.json');
    const oh = this.http.get('assets/ohio_precincts.json');
    const districts = this.http.get('assets/congressional_districts.json');
    const httpRequest = forkJoin([az, wi, oh, districts]);

    const tiles = l.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; ' +
        '<a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19,
      minZoom: 5
    });
    const statesLayer = l.layerGroup(states); // Layer to show the state borders

    this.map = l.map('map', {
      center: [39.8282, -98.5795],
      zoom: 5
    });
    tiles.addTo(this.map);
    statesLayer.addTo(this.map);

    httpRequest.subscribe(data => {
      const statePrecinctsData = [data[0] as any, data[1] as any, data[2] as any];
      const congressionalDistricts = data[3] as any;
      const statePrecincts = {
        AZ: l.geoJSON(statePrecinctsData[0].geometries, {style: precinctStyle}),
        WI: l.geoJSON(statePrecinctsData[1].geometries, {style: precinctStyle}),
        OH: l.geoJSON(statePrecinctsData[2].geometries, {style: precinctStyle})
      };
      let districtsLayer = [];
      const precinctsLayer = [statePrecincts.AZ, statePrecincts.WI, statePrecincts.OH];

      for (const key in congressionalDistricts) {
        if (!congressionalDistricts.hasOwnProperty(key)) { continue; }
        const district = l.geoJSON(congressionalDistricts[key], {style: districtStyle});
        district.on('click', e => {
          this.map.setView(e.latlng, 9);
          this.map.addLayer(statePrecincts[key]);
        });
        districtsLayer.push(district);
      }
      districtsLayer = l.layerGroup(districtsLayer);

      for (const s of states) {
        s.on('click', e => {
          this.map.setView(e.latlng, 7);
          this.map.removeLayer(statesLayer);
          this.map.addLayer(districtsLayer);
        });
      }

      this.map.on('zoomend', e => { // Change which layer is visible based on how zoomed in the map is
        if (this.map.getZoom() <= 5.5) {
          this.map.removeLayer(districtsLayer);
          this.map.addLayer(statesLayer);
        } else if (this.map.getZoom() <= 8) {
          precinctsLayer.forEach(layer => this.map.removeLayer(layer));
        }
      });

      tiles.addTo(this.map);
      l.control.layers({}, {States: statesLayer, 'Congressional Districts': districtsLayer}).addTo(this.map);
    });
  }
}
