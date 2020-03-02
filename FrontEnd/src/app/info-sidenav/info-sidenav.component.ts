import {Component, OnInit, ViewChild} from '@angular/core';
import {MatSidenav} from '@angular/material/sidenav';

@Component({
  selector: 'app-info-sidenav',
  templateUrl: './info-sidenav.component.html',
  styleUrls: ['./info-sidenav.component.css']
})
export class InfoSidenavComponent implements OnInit {
  @ViewChild(MatSidenav)
  public sidenav: MatSidenav;
  constructor() { }

  ngOnInit(): void {
  }

  toggle() {
    this.sidenav.toggle();
  }
}
