import {Component, OnInit, Output, EventEmitter, ViewChildren, QueryList} from '@angular/core';
import {Error} from '../../models/models';
import * as L from 'leaflet';
import {errorStyle} from '../styles';
import {ErrorType} from '../../models/enums';
import {HttpClient} from '@angular/common/http';
import {loadRequest} from '../../PrecinctHelper';
import {MatExpansionPanel} from '@angular/material/expansion';

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
  @ViewChildren(MatExpansionPanel) matPanels: QueryList<MatExpansionPanel>;

  constructor(private http: HttpClient) {
    const capitalizeFirst = (s) => s.charAt(0).toUpperCase() + s.slice(1);
    for (const key of this.errorKeys) {
      this.errorTypeMap[key] = key.toLowerCase().split(/_/g).map(capitalizeFirst).join(' ');
    }
  }

  ngOnInit(): void {
  }

  goToError(error: Error) {
    console.log(error);
    if (this.selectedError !== error) {
     if (error.errorBoundaryGeoJSON) {
       this.map.fitBounds(error.layer.getBounds());
       this.map.addLayer(error.layer);

       if (this.selectedError) {
         this.map.removeLayer(this.selectedError.layer);
       }
     }
     this.goToPrecinct.emit(error.precinctUid);
     this.selectedError = error;
    } else {
     if (this.selectedError.layer) {
       this.map.removeLayer(this.selectedError.layer);
     }
     this.selectedError = undefined;
    }
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
        error.layer.on('click', () => this.goToError(error));
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
    loadRequest(this.http.post('/boundarycorrection/defineghostprecinct', {errID: error.id}, {responseType: 'text'}), id => {
      const p = {uid: id, precinctGeoJSON: JSON.stringify(error.errorBoundaryGeoJSON)};
      this.notify.emit(p);
      error.resolved = true;
    });
  }

  unSelectError() {
    if (this.selectedError.layer) { this.map.removeLayer(this.selectedError.layer); }
    for (const panel of this.matPanels.toArray()) {
      if (panel.expanded) {
        panel.close();
      }
    }
    this.selectedError = undefined;
  }
}
