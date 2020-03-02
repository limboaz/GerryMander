import {Component, ViewChild} from '@angular/core';
import {BreakpointObserver, Breakpoints} from '@angular/cdk/layout';
import {Observable} from 'rxjs';
import {map, shareReplay} from 'rxjs/operators';
import {PrecinctExample} from '../map/precinct.example';

export const selectedStyle = {
  color: '#569335',
  weight: 1,
  opacity: 1.00
};

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent {
  public selectedPrecinct: PrecinctExample;
  public addingNeighbor = false;
  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  constructor(private breakpointObserver: BreakpointObserver) {}

  addNeighbor() {
    this.addingNeighbor = true;
  }

  onNotify(e) {
    if (this.addingNeighbor) {
      this.selectedPrecinct.addNeighbor(e);
      this.addingNeighbor = false;
      this.selectedPrecinct.highlightNeighbors();
      this.selectedPrecinct.highlightNeighbors();
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
