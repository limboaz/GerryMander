import {Component, ViewChild} from '@angular/core';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import {Observable} from 'rxjs';
import {map, shareReplay} from 'rxjs/operators';
import {PrecinctExample} from '../map/precinct.example';
import {MapComponent} from '../map/map.component';

export const selectedStyle = {
  color: '#569335',
  weight: 2,
  opacity: 1.00
};

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  @ViewChild(MapComponent)
  private mapComponent: MapComponent;
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
          this.mapComponent.map.removeLayer(this.selectedPrecinct.layer);
          this.mapComponent.map.removeLayer(e.layer);
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
        this.selectedPrecinct.highlightNeighbors();
        this.selectedPrecinct.highlightNeighbors();
      }
    } else {
      if (this.selectedPrecinct) {
        this.selectedPrecinct.layer.resetStyle();
        this.selectedPrecinct.highlightNeighbors();
      }
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
}
