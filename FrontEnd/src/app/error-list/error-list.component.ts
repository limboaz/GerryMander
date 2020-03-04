import {Component, OnInit, Output, EventEmitter} from '@angular/core';
import {PrecinctExample, selectedStyle} from '../map/precinct.example';
import {MapService} from '../map.service';

@Component({
  selector: 'app-error-list',
  templateUrl: './error-list.component.html',
  styleUrls: ['./error-list.component.css']
})
export class ErrorListComponent implements OnInit {
  public currentErrors;
  public map;
  @Output() combineEvent = new EventEmitter();
  constructor(private mapService: MapService) {
    this.currentErrors = this.mapService.errors;
  }

  ngOnInit(): void {
    this.map = this.mapService.currentMap.subscribe(map => this.map = map);
  }

  goToError(error: PrecinctExample) {
    error.layer.setStyle(selectedStyle);
    error.resetNeighbors();
    error.highlightNeighbors();
    this.map.fitBounds(error.layer.getBounds());
  }

  addMissingNeighbor(error: PrecinctExample) {
    error.addNeighbor(error.missingNeighbor);
    error.resetNeighbors();
    error.highlightNeighbors();
    this.removeError(error);
  }

  removeError(error: PrecinctExample) {
    this.currentErrors = this.currentErrors.filter(e => e !== error);
  }
}
