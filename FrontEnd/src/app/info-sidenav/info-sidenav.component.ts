import {Component, Input, OnInit, ViewChild} from '@angular/core';
import {MatSidenav} from '@angular/material/sidenav';
import {Demographic} from '../demographic.model';
import {Presidential} from '../presidential.model';

@Component({
  selector: 'app-info-sidenav',
  templateUrl: './info-sidenav.component.html',
  styleUrls: ['./info-sidenav.component.css']
})
export class InfoSidenavComponent implements OnInit {
  @ViewChild(MatSidenav)
  public sidenav: MatSidenav;
  @Input() demographicGroups = new Demographic();
  @Input() comment =  '';
  @Input() presidentialGroups = new Presidential();
  constructor() {
    this.demographicGroups.setData('undefined', 0 , 0 , 0 , 0 , 0 , 0 );
    this.presidentialGroups.setData('undefined', 'undefined', 'undefined', 0);
  }

  ngOnInit(): void {
  }

  toggle() {
    this.sidenav.toggle();
  }
}
