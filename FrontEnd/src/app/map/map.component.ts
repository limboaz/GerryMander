import {AfterViewInit, Component} from '@angular/core';
import * as leaf from 'leaflet';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit {
  private map;
  constructor() { }

  ngAfterViewInit(): void {
    const tiles = leaf.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    this.map = leaf.map('map', {
      center: [ 39.8282, -98.5795],
      zoom : 3
    });

    tiles.addTo(this.map);
  }

}
