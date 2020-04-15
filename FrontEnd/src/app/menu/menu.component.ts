import {Component, ViewChild} from '@angular/core';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import {Observable} from 'rxjs';
import {map, shareReplay} from 'rxjs/operators';
import {PrecinctExample, selectedStyle} from '../map/precinct.example';
import {MapComponent} from '../map/map.component';
import {ErrorListComponent} from '../error-list/error-list.component';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  @ViewChild(MapComponent)
  public mapComponent: MapComponent;
  @ViewChild(ErrorListComponent)
  public errorListComponent: ErrorListComponent;
  public selectedPrecinct: PrecinctExample;
  public addingNeighbor = false;
  public combiningPrecincts = false;
  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  constructor(private breakpointObserver: BreakpointObserver) {}

  onNotify(e) {
    if (this.combiningPrecincts) {
      if (this.selectedPrecinct) {
        const combined = PrecinctExample.joinPrecincts(this.selectedPrecinct, e);
        if (combined) {
          combined.layer.addTo(this.mapComponent.map);
          combined.layer.on('click', me => this.mapComponent.exampleOnClick(combined.layer));
          combined.resetNeighbors();
          this.mapComponent.map.removeLayer(this.selectedPrecinct.layer);
          this.mapComponent.map.removeLayer(e.layer);

          if (this.selectedPrecinct.error === 'GHOST' || e.error === 'GHOST') {
            this.errorListComponent.removeError(this.selectedPrecinct);
          }

          this.selectedPrecinct = undefined;
          this.combiningPrecincts = false;
        }
      } else {
        this.selectedPrecinct = e;
        this.selectedPrecinct.layer.setStyle(selectedStyle);
      }
    } else if (this.addingNeighbor) {
      if (this.selectedPrecinct.addNeighbor(e)) {
        this.addingNeighbor = false;
        this.selectedPrecinct.resetNeighbors();
        this.selectedPrecinct.highlightNeighbors();
      }
    } else {
      if (this.selectedPrecinct) {
        this.selectedPrecinct.layer.resetStyle();
        this.selectedPrecinct.resetNeighbors();
      } // a comment
      if (this.selectedPrecinct !== e) {
        this.selectedPrecinct = e;
        this.selectedPrecinct.layer.setStyle(selectedStyle);
        this.selectedPrecinct.highlightNeighbors();
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
