import {AfterViewInit, Component, ViewChild} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import * as L from 'leaflet';
import {icon, Marker} from 'leaflet';
import {InfoSidenavComponent} from '../info-sidenav/info-sidenav.component';
import {ErrorListComponent} from '../error-list/error-list.component';
import {StatePostalCode} from '../../models/enums';
import {CongressionalDistrict, ElectionData, Error, NeighborData, Precinct, State} from '../../models/models';
import {districtStyle, precinctStyle, selectedStyle, stateStyle} from '../styles';
import {addNeighbor, highlightNeighbors, loadRequest, removeNeighbor, resetNeighbors, updateBoundary} from '../../PrecinctHelper';
import {warningMessage, notificationType} from '../../PrecinctHelper';
import {AttributeMenuComponent} from '../attribute-menu/attribute-menu.component';
import './leaflet.shpfile';
import '@geoman-io/leaflet-geoman-free';
import {MatSnackBar, MatSnackBarRef, SimpleSnackBar} from '@angular/material/snack-bar';
import {NotifierService} from 'angular-notifier';

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
  currentDistrictID = -1;

  @ViewChild(InfoSidenavComponent)
  public infoSidenav: InfoSidenavComponent;
  @ViewChild(ErrorListComponent)
  public errorList: ErrorListComponent;
  @ViewChild(AttributeMenuComponent)
  public attrMenu: AttributeMenuComponent;
  private snackBarRef: MatSnackBarRef<SimpleSnackBar>;
  EditState = EditState;
  private prevGeoJSON: any;

  constructor(public http: HttpClient, private snackBar: MatSnackBar,  private notifier: NotifierService) {
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
    this.infoSidenav.errorList = this.errorList;
    tiles.addTo(this.map);
    L.control.zoom({position: 'bottomright'}).addTo(this.map);
    this.marker = L.marker([0, 0]).addTo(this.map);
    this.marker.on('click', () => this.infoSidenav.sidenav.toggle());
    loadRequest(this.http.get<State[]>('/data/getstates'), (states: State[]) => {
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
          this.map.removeLayer(this.errorList.errorsLayer);
        }
      });
      const addStyle = s => `<span class='leaflet-control-labels'>${s}</span>`;
      this.mapControl = L.control.layers({}, {}, {collapsed: false});
      this.mapControl.addOverlay(statesLayer, addStyle('States'));
      this.mapControl.addOverlay(this.districtsLayer, addStyle('Districts'));
      this.mapControl.addOverlay(this.errorList.errorsLayer, addStyle('Error'));
      this.mapControl.addOverlay(this.precinctsLayer, addStyle('Precincts'));
      this.mapControl.addTo(this.map);

      this.http.get('/data/getnationalparksdata', {responseType: 'arraybuffer'}).subscribe(d => {
        const parksLayer = new L.Shapefile(d,
          {onEachFeature: (feature, layer) => layer.bindPopup(feature.properties.UNIT_NAME)});
        this.mapControl.addOverlay(parksLayer, addStyle('National Parks'));
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

    loadRequest(this.http.get<CongressionalDistrict[]>(`/data/getcongbystate?state=${state}`),
      (congressionalDistricts: CongressionalDistrict[]) => {
        console.log(congressionalDistricts);
        // alternatively display all the precinct boundaries at this point instead of district ones
        const districtGeoJSONs = congressionalDistricts.map(d => {
          d.congressionalDistrictGeoJSON = JSON.parse(d.congressionalDistrictGeoJSON);
          d.congressionalDistrictGeoJSON.properties = {districtID: d.id, districtNum: d.districtNum};
          return d.congressionalDistrictGeoJSON;
        });

        const onEachDistrictFeature = (feature, layer) => {
          layer.on({
            click: e => this.getPrecincts(feature.properties.districtID),
            mouseover: e => layer.bindTooltip('District Number: ' + feature.properties.districtNum).openTooltip()
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

  getPrecincts(districtID: number): void {
    if (this.currentDistrictID === districtID) {
      console.log(this.precinctsLayer);
      this.map.addLayer(this.precinctsLayer);
      return;
    }
    this.map.removeLayer(this.precinctsLayer);

    loadRequest(this.http.get<Precinct[]>(`/data/getprecinctsbycong?congressionalID=${districtID}`),
      (precincts: Precinct[]) => {
        this.uidToPrecinctMap = {};
        this.precinctsLayer.clearLayers();
        for (const p of precincts) {
          this.initializePrecinct(p);
        }
        this.currentDistrictID = districtID;
        this.map.addLayer(this.precinctsLayer);
      });
  }

  initializePrecinct(p: Precinct) {
    p.precinctGeoJSON = JSON.parse(p.precinctGeoJSON);
    p.precinctGeoJSON.properties = {uid: p.uid};
    try {
      p.layer = L.geoJSON(p.precinctGeoJSON, {style: precinctStyle});
    } catch (e) {
      console.log(p.precinctGeoJSON);
      return;
    }
    p.layer.wrapperPrecinct = p;
    p.layer.on({
      click: this.onPrecinctClick(p.precinctGeoJSON, p.layer),
      mouseover: this.onPrecinctMouseOver(p.precinctGeoJSON, p.layer)
    });
    this.precinctsLayer.addLayer(p.layer);
    this.uidToPrecinctMap[p.uid] = p;
  }

  onPrecinctClick(feature, layer) {
    return (e) => {
      this.selectPrecinct(this.uidToPrecinctMap[feature.properties.uid]);

      if (!this.modifyingPrecinct) {
        this.marker.setLatLng(e.latlng);
        this.getPrecinctData(feature.properties.uid);
      }
    };
  }

  onPrecinctMouseOver(feature, layer) {
    return () => layer.bindTooltip('Name: ' + layer.wrapperPrecinct.name
      + '</br> Total Population: ' + layer.wrapperPrecinct.populationData.total.toLocaleString()).openTooltip();
  }

  getPrecinctData(uid: string) {
    this.infoSidenav.precinctID = uid;

    if (this.uidToPrecinctMap[uid].populationData) {
      this.infoSidenav.populationData = this.uidToPrecinctMap[uid].populationData;
    }

    if (this.uidToPrecinctMap[uid].electionData) {
      this.infoSidenav.addElectionData(this.uidToPrecinctMap[uid].electionData);
      return;
    }
    this.infoSidenav.addElectionData([]);
    loadRequest(this.http.get<ElectionData[]>(`/data/getelectiondata?uid=${uid}`),
      (electionData: ElectionData[]) => {
        this.uidToPrecinctMap[uid].electionData = electionData;
        this.infoSidenav.addElectionData(this.uidToPrecinctMap[uid].electionData);
      });
  }

  commit(state: EditState) {
    switch (state) {
      case EditState.MERGING_PRECINCTS:
        if (!this.errorList.selectedError) {
          this.notifier.notify(notificationType, warningMessage);
          break;
        }

        const precinctA = this.selectedPrecinct;
        const precinctB = this.otherSelectedPrecinct;
        loadRequest(this.http.post(`/boundarycorrection/mergeprecincts?precinctA=${precinctA.uid}&precinctB=${precinctB.uid}` +
          `&errID=${this.errorList.selectedError.id}`, {}),
          (precinct: Precinct) => {
            if (precinct) {
              this.initializePrecinct(precinct);
              this.precinctsLayer.removeLayer(precinctA.layer);
              this.precinctsLayer.removeLayer(precinctB.layer);
              resetNeighbors(precinct, this.uidToPrecinctMap);
              this.map.removeLayer(precinctA.layer);
              this.map.removeLayer(precinctB.layer);
              this.selectedPrecinct = precinct;
              this.selectedPrecinct.layer.setStyle(selectedStyle);
              this.errorList.selectedError.resolved = true;
            }
          });
        break;
      case EditState.ADDING_NEIGHBOR:
        addNeighbor(this.http, this.selectedPrecinct, this.otherSelectedPrecinct, this.uidToPrecinctMap);
        break;
      case EditState.REMOVING_NEIGHBOR:
        const removed = removeNeighbor(this.http, this.selectedPrecinct, this.otherSelectedPrecinct, this.uidToPrecinctMap);
        if (!removed) { this.notifier.notify('error', 'Not a valid neighbor to remove'); }
        break;
      case EditState.EDIT_BOUNDARY || EditState.CREATE_BOUNDARY:
        if (!this.errorList.selectedError) {
          this.notifier.notify(notificationType, warningMessage);
          break;
        }
        this.prevGeoJSON = undefined;
        updateBoundary(this.http, this.selectedPrecinct, this.selectedPrecinct.layer.toGeoJSON(), this.errorList.selectedError.id);
        this.errorList.selectedError.resolved = true;
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

  goToPrecinct(precinctUid) {
    if (this.uidToPrecinctMap[precinctUid]) {
      this.map.addLayer(this.uidToPrecinctMap[precinctUid].layer);
      this.map.fitBounds(this.uidToPrecinctMap[precinctUid].layer.getBounds());
      this.selectPrecinct(this.uidToPrecinctMap[precinctUid]);
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
