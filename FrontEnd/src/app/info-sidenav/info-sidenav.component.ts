import {Component, Input, OnInit, Output, ViewChild} from '@angular/core';
import {MatSidenav} from '@angular/material/sidenav';
import {Demographic} from '../demographic.model';
import {DialogButtonComponent} from '../dialog-button/dialog-button.component';
import {ElectionData} from '../presidential.model';

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
  @Input() presidentialData: ElectionData;
  public congressionalData = [];

  constructor() {
    this.demographicGroups.setData('undefined', 0 , 0 , 0 , 0 , 0 , 0 );
  }

  ngOnInit(): void {
  }

  toggle() {
    this.sidenav.toggle();
  }
}
