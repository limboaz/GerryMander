import {AfterViewInit, Component, ViewChild} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import * as l from 'leaflet';
import {icon, Marker} from 'leaflet';
import {InfoSidenavComponent} from '../info-sidenav/info-sidenav.component';
import {ErrorListComponent} from '../error-list/error-list.component';
import {StatePostalCode} from '../../models/enums';
import {CongressionalDistrict, Precinct, State, Error, ElectionData} from '../../models/models';
import {districtStyle, precinctStyle, selectedStyle, stateStyle} from '../styles';
import {addNeighbor, highlightNeighbors, mergePrecincts, resetNeighbors} from '../../PrecinctHelper';
import {AttributeMenuComponent} from '../attribute-menu/attribute-menu.component';

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

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {
  public map;
  public districtsLayer = l.layerGroup();
  public currentStatePrecincts;
  public currentDistrictsPrecincts;
  public mapControl;
  public marker;
  public stateCache = {};
  public uidToPrecinctMap = {};
  public addingNeighbor: boolean;
  public combiningPrecincts: boolean;
  public selectedPrecinct: Precinct;

  @ViewChild(InfoSidenavComponent)
  public infoSidenav: InfoSidenavComponent;
  @ViewChild(ErrorListComponent)
  public errorList: ErrorListComponent;
  @ViewChild(AttributeMenuComponent)
  public attrMenu: AttributeMenuComponent;

  constructor(private http: HttpClient) {
  }

  ngAfterViewInit(): void {
    const tiles = l.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; '
        + '<a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19,
      minZoom: 5
    });
    this.map = l.map('map', {
      center: [39.8282, -98.5795],
      zoom: 5,
      zoomControl: false
    });
    this.errorList.map = this.map;
    tiles.addTo(this.map);
    l.control.zoom({position: 'bottomright'}).addTo(this.map);
    this.marker = l.marker([0, 0]).addTo(this.map);
    this.marker.on('click', () => this.infoSidenav.sidenav.toggle());

    this.http.get<State[]>('/data/getstates').subscribe((states: State[]) => {
      const statesLayer = l.layerGroup();

      states.forEach((s) => {
        const layer = l.geoJSON(JSON.parse(s.stateGeoJSON), {style: stateStyle});
        statesLayer.addLayer(layer);
        layer.on('click', this.onStateClick(statesLayer, s.state));
      });

      statesLayer.addTo(this.map);

      this.map.on('zoomend', e => { // Change which layer is visible based on how zoomed in the map is
        if (this.map.getZoom() <= 5.5) {
          this.map.removeLayer(this.districtsLayer);
          this.map.addLayer(statesLayer);
        } else if (this.map.getZoom() <= 8) {
          if (this.currentDistrictsPrecincts) {
            this.map.removeLayer(this.currentDistrictsPrecincts.layerGroup);
          }
        }
      });
      this.mapControl = l.control.layers({}, {States: statesLayer});
      this.mapControl.addTo(this.map);
    });
  }

  getCongressionalDistricts(state: StatePostalCode): void {
    if (this.stateCache[state]) {
      this.map.addLayer(this.districtsLayer);
      return;
    }

    this.http.get<CongressionalDistrict[]>(`/data/getcongbystate?state=${state}`)
      .subscribe((congressionalDistricts: CongressionalDistrict[]) => {
        console.log(congressionalDistricts);
        // alternatively display all the precinct boundaries at this point instead of district ones
        const districtGeoJSONs = congressionalDistricts.map(d => {
          d.congressionalDistrictGeoJSON = JSON.parse(d.congressionalDistrictGeoJSON);
          d.congressionalDistrictGeoJSON.properties = {districtNum: d.districtNum};
          return d.congressionalDistrictGeoJSON;
        });

        const onEachDistrictFeature = (feature, layer) => {
          layer.on('click', e => {
            this.map.setView(e.latlng, 9);
            this.getPrecincts(feature.properties.districtNum);
          });
        };
        const district = l.geoJSON(districtGeoJSONs, {style: districtStyle, onEachFeature: onEachDistrictFeature});

        this.districtsLayer.addLayer(district);
        this.stateCache[state] = congressionalDistricts;
        this.map.addLayer(this.districtsLayer);
        this.mapControl.addOverlay(this.districtsLayer, 'Districts');
      });
  }

  getErrors(state: StatePostalCode) {
    this.http.get<Error[]>(`/data/geterrors?state=${state}`).subscribe((errors: Error[]) => {
      this.mapControl.addOverlay(this.errorList.addErrors(errors), 'Errors');
    });
  }

  onStateClick(statesLayer, state: StatePostalCode) {
    return e => {
      this.map.setView(e.latlng, 7);
      this.map.removeLayer(statesLayer);
      this.getCongressionalDistricts(state);
      this.getErrors(state);
    };
  }

  onPrecinctClick(feature, layer) {
    return (e) => {
      // load the info of this feature to infoSidenav here
      this.marker.setLatLng(e.latlng);
      this.getPrecinctData(layer.wrapperPrecinct, feature.properties.uid);
    };
  }

  onPrecinctMouseOver(feature, layer) {
    return () => layer.bindTooltip('Name: ' + layer.wrapperPrecinct.name
      + ' Total Population: ' + layer.wrapperPrecinct.populationData.total).openTooltip();
  }

  getPrecincts(districtNum: number): void {
    if (this.currentDistrictsPrecincts) {
      if (this.currentDistrictsPrecincts.districtNum === districtNum) {
        this.map.addLayer(this.currentDistrictsPrecincts.layerGroup);
        return;
      }

      this.map.removeLayer(this.currentDistrictsPrecincts.layerGroup);
    }

    this.http.get<Precinct[]>(`/data/getprecinctsbycong?congressionalID=${districtNum}`)
      .subscribe((precincts: Precinct[]) => {
        this.uidToPrecinctMap = {};
        const precinctLayers = precincts.map(p => {
          p.precinctGeoJSON = JSON.parse(p.precinctGeoJSON);
          p.precinctGeoJSON.properties = {uid: p.uid};
          const precinctLayer = l.geoJSON(p.precinctGeoJSON, {style: precinctStyle});
          p.layer = precinctLayer;
          precinctLayer.wrapperPrecinct = p;
          precinctLayer.on({
            click: this.onPrecinctClick(p.precinctGeoJSON, precinctLayer),
            mouseover: this.onPrecinctMouseOver(p.precinctGeoJSON, precinctLayer)
          });
          this.uidToPrecinctMap[p.uid] = p;
          return precinctLayer;
        });
        this.currentDistrictsPrecincts = {
          districtNum,
          precincts,
          layerGroup: l.layerGroup(precinctLayers)
        };
        this.mapControl.addOverlay(this.currentDistrictsPrecincts.layerGroup, 'Precincts');
        this.map.addLayer(this.currentDistrictsPrecincts.layerGroup);
      });
  }

  getPrecinctData(wrapperPrecinct: Precinct, uid: string) {
    if (this.uidToPrecinctMap[uid].electionData) {
      this.infoSidenav.addData(this.uidToPrecinctMap[uid].populationData, this.uidToPrecinctMap[uid].electionData);
      this.selectPrecinct(wrapperPrecinct);
      return;
    }

    this.http.get<ElectionData[]>(`/data/getelectiondata?uid=${uid}`)
      .subscribe((electionData: ElectionData[]) => {
        this.uidToPrecinctMap[uid].electionData = electionData;
        this.infoSidenav.addData(this.uidToPrecinctMap[uid].populationData, this.uidToPrecinctMap[uid].electionData);
        this.selectPrecinct(wrapperPrecinct);
      });
  }

  selectPrecinct(precinct: Precinct) {
    if (this.combiningPrecincts) {
      if (this.selectedPrecinct) {
        const combined = mergePrecincts(this.selectedPrecinct, precinct);
        if (combined) {
          combined.layer.addTo(this.map);
          combined.layer.on('click', this.onPrecinctClick(combined.precinctGeoJSON, combined.layer));
          resetNeighbors(combined, this.currentDistrictsPrecincts);
          this.map.removeLayer(this.selectedPrecinct.layer);
          this.map.removeLayer(precinct.layer);

          this.selectedPrecinct = undefined;
          this.combiningPrecincts = false;
        }
      } else {
        this.selectedPrecinct = precinct;
        this.selectedPrecinct.layer.setStyle(selectedStyle);
      }
    } else if (this.addingNeighbor) {
      addNeighbor(this.selectedPrecinct, precinct);
      this.addingNeighbor = false;
      resetNeighbors(this.selectedPrecinct, this.currentDistrictsPrecincts);
      highlightNeighbors(this.selectedPrecinct, this.currentDistrictsPrecincts);
    } else {
      if (this.selectedPrecinct) {
        this.selectedPrecinct.layer.resetStyle();
        resetNeighbors(this.selectedPrecinct, this.currentDistrictsPrecincts);
      } // a comment
      if (this.selectedPrecinct !== precinct) {
        this.selectedPrecinct = precinct;
        this.selectedPrecinct.layer.setStyle(selectedStyle);
        highlightNeighbors(this.selectedPrecinct, this.currentDistrictsPrecincts);
      } else {
        this.selectedPrecinct = undefined;
      }
    }
  }

  cancelAdd() {
    this.addingNeighbor = false;
  }

  cancelCombine() {
    this.combiningPrecincts = false;
    this.selectedPrecinct = undefined;
  }
}
