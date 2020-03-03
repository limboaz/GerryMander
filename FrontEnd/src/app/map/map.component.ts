import {AfterViewInit, Component, ViewChild, EventEmitter, Output} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {forkJoin} from 'rxjs';
import * as l from 'leaflet';
import {exampleLayerGroup, precinctStyle} from './precinct.example';
import * as statesGeoJSON from '../../assets/us_states_500K.json';
import {InfoSidenavComponent} from '../info-sidenav/info-sidenav.component';
import {icon, Marker} from 'leaflet';

const iconRetinaUrl = 'assets/marker-icon-2x.png';
const iconUrl = 'assets/marker-icon.png';
const shadowUrl = 'assets/marker-shadow.png';
const iconDefault = icon({
  iconRetinaUrl,
  iconUrl,
  shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});
Marker.prototype.options.icon = iconDefault;

const stateStyle = {
  color: '#ff7800',
  weight: 5,
  opacity: 0.65
};

const districtStyle = {
  color: '#ff95f8',
  weight: 2,
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
  public map;
  public exampleLayerGroup;
  @Output() notify = new EventEmitter();
  @ViewChild(InfoSidenavComponent)
  public infoSidenav: InfoSidenavComponent;


  constructor(private http: HttpClient) {
  }

  exampleOnClick(layer) {
    this.notify.emit(layer.wrapperPrecinct);
  }

  ngAfterViewInit(): void {
    // const az = this.http.get('assets/arizona.json');
    const wi = this.http.get('assets/wi_example.json');
    const oh = this.http.get('assets/oh_example.json');
    const az = this.http.get('assets/az_example.json');
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
      zoom: 5,
      zoomControl: false
    });
    tiles.addTo(this.map);
    statesLayer.addTo(this.map);
    this.exampleLayerGroup = exampleLayerGroup;
    this.exampleLayerGroup.eachLayer(layer => layer.on('click', e => this.exampleOnClick(layer)));
    l.control.zoom({position: 'bottomright'}).addTo(this.map);
    const marker = l.marker([0, 0]).addTo(this.map);
    marker.on('click', e => this.infoSidenav.toggle());
    const onMapClick = (feature, layer) => {
      return e => {
        marker.setLatLng(e.latlng);
        // load the info of this feature to infoSidenav here
      };
    };
    const onMouseOver = (feature, layer) => {
      console.log(feature);
      return e => layer.bindTooltip(feature.properties.name).openTooltip();
    };
    const onEachFeature = (feature, layer) => {
      layer.on({
        click: onMapClick(feature, layer),
        mouseover: onMouseOver(feature, layer)
      });
    };

    httpRequest.subscribe(data => {
      const statePrecinctsData = [data[0] as any, data[1] as any, data[2] as any];
      const congressionalDistricts = data[3] as any;
      const statePrecincts = {
        AZ: l.geoJSON(statePrecinctsData[0], {style: precinctStyle, onEachFeature}),
        WI: l.geoJSON(statePrecinctsData[1], {style: precinctStyle, onEachFeature}),
        OH: l.geoJSON(statePrecinctsData[2], {style: precinctStyle, onEachFeature})
      };
      const precinctsLayer = [statePrecincts.AZ, statePrecincts.OH, statePrecincts.WI];
      let districtsLayer = [];

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
      l.control.layers({}, {
        States: statesLayer,
        'Congressional Districts': districtsLayer,
        'Example Layer': exampleLayerGroup
      }).addTo(this.map);
    }, error => {
      l.control.layers({}, {States: statesLayer, 'Example Layer': exampleLayerGroup}).addTo(this.map);
      console.log('error retrieving boundaries', error);
    });
  }
}
