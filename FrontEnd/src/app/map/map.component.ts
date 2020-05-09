import {AfterViewInit, Component, ViewChild} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import * as L from 'leaflet';
import {icon, Marker} from 'leaflet';
import {InfoSidenavComponent} from '../info-sidenav/info-sidenav.component';
import {ErrorListComponent} from '../error-list/error-list.component';
import {StatePostalCode} from '../../models/enums';
import {CongressionalDistrict, Precinct, State, Error, ElectionData, NeighborData} from '../../models/models';
import {districtStyle, precinctStyle, selectedStyle, stateStyle} from '../styles';
import {addNeighbor, removeNeighbor, highlightNeighbors, mergePrecincts, resetNeighbors} from '../../PrecinctHelper';
import {AttributeMenuComponent} from '../attribute-menu/attribute-menu.component';
import './leaflet.shpfile';
import '@geoman-io/leaflet-geoman-free';
import {MatSnackBar, MatSnackBarRef, SimpleSnackBar} from '@angular/material/snack-bar';

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
  map;
  mapControl;
  marker;
  stateCache = {};
  uidToPrecinctMap = {};
  districtsLayer = L.layerGroup();
  precinctsLayer = L.layerGroup();
  modifyingPrecinct: boolean;
  selectedPrecinct: Precinct;
  otherSelectedPrecinct: Precinct;
  currentDistrictNum = -1;

  @ViewChild(InfoSidenavComponent)
  public infoSidenav: InfoSidenavComponent;
  @ViewChild(ErrorListComponent)
  public errorList: ErrorListComponent;
  @ViewChild(AttributeMenuComponent)
  public attrMenu: AttributeMenuComponent;
  private snackBarRef: MatSnackBarRef<SimpleSnackBar>;
  EditState = EditState;
  private prevGeoJSON: any;

  constructor(private http: HttpClient, private snackBar: MatSnackBar) {
  }

  ngAfterViewInit(): void {
    const tiles = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; '
        + '<a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19,
      minZoom: 5
    });
    this.map = L.map('map', {
      center: [39.8282, -98.5795],
      zoom: 5,
      zoomControl: false
    });
    this.errorList.map = this.map;
    tiles.addTo(this.map);
    L.control.zoom({position: 'bottomright'}).addTo(this.map);
    this.marker = L.marker([0, 0]).addTo(this.map);
    this.marker.on('click', () => this.infoSidenav.sidenav.toggle());
    this.loadRequest(this.http.get<State[]>('/data/getstates'), (states: State[]) => {
      const statesLayer = L.layerGroup();

      states.forEach((s) => {
        const layer = L.geoJSON(JSON.parse(s.stateGeoJSON), {style: stateStyle});
        layer.pm.enable({allowSelfIntersection: false});
        statesLayer.addLayer(layer);
        this.stateCache[s.state] = s;
        s.layer = layer;
        layer.on('click', () => this.goToState(s.state));
      });

      statesLayer.addTo(this.map);

      this.map.on('zoomend', e => { // Change which layer is visible based on how zoomed in the map is
        if (this.map.getZoom() < 7) {
          if (this.precinctsLayer.getLayers().length > 0) {
            this.map.removeLayer(this.precinctsLayer);
          }
          this.map.removeLayer(this.districtsLayer);
          this.marker.setLatLng([0, 0]);
          this.infoSidenav.sidenav.close();
          this.selectedPrecinct = undefined;
        }
      });
      this.mapControl = L.control.layers({}, {
        States: statesLayer,
        Districts: this.districtsLayer,
        Error: this.errorList.errorsLayer,
        Precincts: this.precinctsLayer
      });
      this.mapControl.addTo(this.map);

      this.http.get('/data/getnationalparksdata', {responseType: 'arraybuffer'}).subscribe(d => {
        const parksLayer = new L.Shapefile(d);
        this.mapControl.addOverlay(parksLayer, 'National Parks');
      });
    });
  }

  goToState(state: StatePostalCode) {
    this.map.fitBounds(this.stateCache[state].layer.getBounds());
    this.getCongressionalDistricts(state);
    this.getErrors(state);
  }

  getCongressionalDistricts(state: StatePostalCode): void {
    if (this.stateCache[state].congressionalDistricts) {
      if (!this.map.hasLayer(this.districtsLayer)) { this.map.addLayer(this.districtsLayer); }
      return;
    }

    this.loadRequest(this.http.get<CongressionalDistrict[]>(`/data/getcongbystate?state=${state}`),
      (congressionalDistricts: CongressionalDistrict[]) => {
        console.log(congressionalDistricts);
        // alternatively display all the precinct boundaries at this point instead of district ones
        const districtGeoJSONs = congressionalDistricts.map(d => {
          d.congressionalDistrictGeoJSON = JSON.parse(d.congressionalDistrictGeoJSON);
          d.congressionalDistrictGeoJSON.properties = {districtNum: d.id};
          return d.congressionalDistrictGeoJSON;
        });

        const onEachDistrictFeature = (feature, layer) => {
          layer.on('click', e => {
            console.log(feature.properties.districtNum);
            this.getPrecincts(feature.properties.districtNum);
          });
        };
        const district = L.geoJSON(districtGeoJSONs, {style: districtStyle, onEachFeature: onEachDistrictFeature});

        this.districtsLayer.addLayer(district);
        this.stateCache[state].congressionalDistricts = congressionalDistricts;
        this.map.addLayer(this.districtsLayer);
      });
  }

  getErrors(state: StatePostalCode) {
    this.http.get<Error[]>(`/data/geterrors?state=${state}`).subscribe((errors: Error[]) => {
      this.errorList.addErrors(errors);
    });
  }

  getPrecincts(districtNum: number): void {
    if (this.currentDistrictNum === districtNum) {
      this.map.addLayer(this.precinctsLayer);
      return;
    }
    this.map.removeLayer(this.precinctsLayer);

    this.loadRequest(this.http.get<Precinct[]>(`/data/getprecinctsbycong?congressionalID=${districtNum}`),
      (precincts: Precinct[]) => {
        this.uidToPrecinctMap = {};
        const precinctLayers = precincts.map(p => {
          p.precinctGeoJSON = JSON.parse(p.precinctGeoJSON);
          p.precinctGeoJSON.properties = {uid: p.uid};
          const precinctLayer = L.geoJSON(p.precinctGeoJSON, {style: precinctStyle});
          p.layer = precinctLayer;
          precinctLayer.wrapperPrecinct = p;
          precinctLayer.on({
            click: this.onPrecinctClick(p.precinctGeoJSON, precinctLayer),
            mouseover: this.onPrecinctMouseOver(p.precinctGeoJSON, precinctLayer)
          });
          this.uidToPrecinctMap[p.uid] = p;
          return precinctLayer;
        });
        this.currentDistrictNum = districtNum;
        this.precinctsLayer.clearLayers();
        this.precinctsLayer.addLayer(L.layerGroup(precinctLayers));
        this.map.addLayer(this.precinctsLayer);
      });
  }

  onPrecinctClick(feature, layer) {
    return (e) => {
      this.selectPrecinct(this.uidToPrecinctMap[feature.properties.uid]);

      if (!this.modifyingPrecinct) {
        this.marker.setLatLng(e.latlng);
        this.getPrecinctData(layer.wrapperPrecinct, feature.properties.uid);
      }
    };
  }

  onPrecinctMouseOver(feature, layer) {
    return () => layer.bindTooltip('Name: ' + layer.wrapperPrecinct.name
      + ' Total Population: ' + layer.wrapperPrecinct.populationData.total.toLocaleString()).openTooltip();
  }

  getPrecinctData(wrapperPrecinct: Precinct, uid: string) {
    this.infoSidenav.precinctID = uid;

    if (this.uidToPrecinctMap[uid].populationData) {
      this.infoSidenav.populationData = this.uidToPrecinctMap[uid].populationData;
    }

    if (this.uidToPrecinctMap[uid].electionData) {
      this.infoSidenav.addElectionData(this.uidToPrecinctMap[uid].electionData);
      return;
    }
    this.loadRequest(this.http.get<ElectionData[]>(`/data/getelectiondata?uid=${uid}`),
      (electionData: ElectionData[]) => {
        this.uidToPrecinctMap[uid].electionData = electionData;
        this.infoSidenav.addElectionData(this.uidToPrecinctMap[uid].electionData);
      });
  }

  commit(state: EditState) {
    console.log(state);
    switch (state) {
      case EditState.MERGING_PRECINCTS:
          const combined = mergePrecincts(this.selectedPrecinct, this.otherSelectedPrecinct);
          if (combined) {
            combined.layer.addTo(this.map);
            combined.layer.on('click', this.onPrecinctClick(combined.precinctGeoJSON, combined.layer));
            resetNeighbors(combined, this.uidToPrecinctMap);
            this.map.removeLayer(this.selectedPrecinct.layer);
            this.map.removeLayer(this.otherSelectedPrecinct.layer);
          }
          break;
      case EditState.ADDING_NEIGHBOR:
        addNeighbor(this.selectedPrecinct, this.otherSelectedPrecinct, this.uidToPrecinctMap);
        break;
      case EditState.REMOVING_NEIGHBOR:
        removeNeighbor(this.selectedPrecinct, this.otherSelectedPrecinct, this.uidToPrecinctMap);
        break;
      case EditState.EDIT_BOUNDARY:
        this.prevGeoJSON = undefined;
        break;
      case EditState.CREATE_BOUNDARY:
        this.prevGeoJSON = undefined;
        break;
      default:
        console.log('Invalid State');
    }
    this.cancelState();
  }

  selectPrecinct(precinct: Precinct) {
    if (this.modifyingPrecinct) {
      if (precinct === this.selectedPrecinct) { return; }
      if (this.otherSelectedPrecinct) { this.otherSelectedPrecinct.layer.resetStyle(); }
      this.otherSelectedPrecinct = precinct;
      this.otherSelectedPrecinct.layer.setStyle(selectedStyle);
      return;
    }
    if (precinct.neighbors) {
      if (this.selectedPrecinct) {
        this.selectedPrecinct.layer.resetStyle();
        resetNeighbors(this.selectedPrecinct, this.uidToPrecinctMap);
      }
      if (this.selectedPrecinct !== precinct) {
        this.selectedPrecinct = precinct;
        this.selectedPrecinct.layer.setStyle(selectedStyle);
        highlightNeighbors(this.selectedPrecinct, this.uidToPrecinctMap);
      } else {
        this.selectedPrecinct = undefined;
      }
    } else {
      this.http.get<NeighborData[]>(`/data/getprecinctneighbors?uid=${precinct.uid}`).subscribe((neighbors: NeighborData[]) => {
        precinct.neighbors = neighbors;
        this.selectPrecinct(precinct);
      });
    }
  }

  loadRequest(httpRequest, successCallback) {
    const leafletStyle = document.getElementById('leafletStyle');
    leafletStyle.innerHTML = '';
    leafletStyle.appendChild(document.createTextNode('.leaflet-interactive, #map { cursor: wait !important; }'));
    httpRequest.subscribe(d => {
      leafletStyle.innerHTML = '';
      leafletStyle.appendChild(document.createTextNode('.leaflet-interactive, #map { cursor: auto; }'));
      successCallback(d);
    }, () => {
      leafletStyle.innerHTML = '';
      leafletStyle.appendChild(document.createTextNode('.leaflet-interactive, #map { cursor: auto; }'));
    });
  }

  cancelState() {
    if (this.snackBarRef) { this.snackBarRef.dismiss(); }
    if (this.otherSelectedPrecinct) {
      this.otherSelectedPrecinct.layer.resetStyle();
      this.otherSelectedPrecinct = undefined;
      highlightNeighbors(this.selectedPrecinct, this.uidToPrecinctMap);
    }
    this.selectedPrecinct.layer.pm.disable();
    this.map.pm.disableDraw('Polygon');
    this.modifyingPrecinct = false;
    if (this.prevGeoJSON) {
      this.selectedPrecinct.layer.clearLayers();
      this.selectedPrecinct.layer.addData(this.prevGeoJSON);
      this.selectedPrecinct.layer.setStyle(selectedStyle);
      this.prevGeoJSON = undefined;
    }
  }

  changeState(state: EditState, message: string) {
    this.cancelState();
    this.modifyingPrecinct = true;
    this.snackBarRef = this.snackBar.open(message, 'Commit');
    this.snackBarRef.onAction().subscribe(() => this.commit(state));
    this.prevGeoJSON = this.selectedPrecinct.layer.toGeoJSON();

    switch (state) {
      case EditState.CREATE_BOUNDARY:
        this.map.pm.enableDraw('Polygon', {
          snapDistance: 10,
          allowSelfIntersection: false
        });

        this.map.on('pm:create', (e) => {
          const newBoundary = e.layer.toGeoJSON();
          this.selectedPrecinct.layer.clearLayers();
          this.selectedPrecinct.layer.addData(newBoundary);
          this.map.removeLayer(e.layer);
        });
        break;
      case EditState.EDIT_BOUNDARY:
        this.selectedPrecinct.layer.pm.enable({allowSelfIntersection: false});
        break;
    }
  }
}

enum EditState {
  MERGING_PRECINCTS,
  ADDING_NEIGHBOR,
  REMOVING_NEIGHBOR,
  EDIT_BOUNDARY,
  CREATE_BOUNDARY
}
