import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {Error} from '../../models/models';
import * as l from 'leaflet';
import {errorStyle, selectedStyle} from '../styles';
import {ErrorType} from '../../models/enums';

@Component({
  selector: 'app-error-list',
  templateUrl: './error-list.component.html',
  styleUrls: ['./error-list.component.css']
})
export class ErrorListComponent implements OnInit {
  public currentErrors = {};
  public errorKeys = Object.keys(ErrorType).filter(e => !isNaN(Number(ErrorType[e])));
  public errorsLayer = l.layerGroup();
  public map;
  @Output() notify = new EventEmitter();
  constructor() {}

  ngOnInit(): void {
  }

  goToError(error: Error) {
    error.layer.setStyle(selectedStyle);
    this.map.fitBounds(error.layer.getBounds());
    this.map.addLayer(this.errorsLayer);
  }

  removeError(error: Error) {
    this.currentErrors[error.type] = this.currentErrors[error.type].filter(e => e !== error);
  }

  addErrors(errors: Error[]) {
    for (const error of errors) {
      if (error.errorBoundaryGeoJSON) {
        error.errorBoundaryGeoJSON = JSON.parse(error.errorBoundaryGeoJSON);
        error.layer = l.geoJSON(error.errorBoundaryGeoJSON, {style: errorStyle});
        this.errorsLayer.addLayer(error.layer);
      }
      if (this.currentErrors[error.type]) {
        this.currentErrors[error.type].push(error);
      } else {
        this.currentErrors[error.type] = [error];
      }
    }
    console.log(this.currentErrors);
    return this.errorsLayer;
  }
}
