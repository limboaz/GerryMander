import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {Error} from '../../models/models';
import * as L from 'leaflet';
import {errorStyle} from '../styles';
import {ErrorType} from '../../models/enums';
import {HttpClient} from '@angular/common/http';
import {loadRequest} from '../../PrecinctHelper';

@Component({
  selector: 'app-error-list',
  templateUrl: './error-list.component.html',
  styleUrls: ['./error-list.component.css']
})
export class ErrorListComponent implements OnInit {
  public currentErrors = {};
  public errorKeys = Object.keys(ErrorType).filter(e => !isNaN(Number(ErrorType[e])));
  public errorsLayer = L.layerGroup();
  public selectedError: Error;
  public map;
  errorTypeMap = {};
  @Output() notify = new EventEmitter();
  @Output() goToPrecinct = new EventEmitter();

  constructor(private http: HttpClient) {
    const capitalizeFirst = (s) => s.charAt(0).toUpperCase() + s.slice(1);
    for (const key of this.errorKeys) {
      this.errorTypeMap[key] = key.toLowerCase().split(/_/g).map(capitalizeFirst).join(' ');
    }
  }

  ngOnInit(): void {
  }

  goToError(error: Error) {
    if (error.errorBoundaryGeoJSON) {
      this.map.fitBounds(error.layer.getBounds());
      this.map.addLayer(error.layer);
    }
    this.goToPrecinct.emit(error.precinctUid);
    this.selectedError = error;
  }

  addErrors(errors: Error[]) {
    this.errorsLayer.clearLayers();
    for (const errorType of this.errorKeys) {
      this.currentErrors[errorType] = [];
    }
    for (const error of errors) {
      if (error.errorBoundaryGeoJSON) {
        error.errorBoundaryGeoJSON = JSON.parse(error.errorBoundaryGeoJSON);
        error.layer = L.geoJSON(error.errorBoundaryGeoJSON, {style: errorStyle});
        this.errorsLayer.addLayer(error.layer);
      }
      if (this.currentErrors[error.type]) {
        this.currentErrors[error.type].push(error);
      } else {
        this.currentErrors[error.type] = [error];
      }
    }
    return this.errorsLayer;
  }

  defineGhostPrecinct(error: Error) {
    loadRequest(this.http.post('/boundarycorrection/defineghostprecinct', {errID: error.id}), id => {
      const p = {uid: id, precinctGeoJSON: JSON.stringify(error.errorBoundaryGeoJSON)};
      this.notify.emit(p);
      error.resolved = true;
    });
  }

  resolveError(error: Error) {
    error.resolved = true;
  }
}
