import {Component, OnInit, ViewChild} from '@angular/core';
import {MatSidenav} from '@angular/material/sidenav';
import {PopulationData, ElectionData} from '../../models/models';
import {ElectionType} from '../../models/enums';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {ErrorListComponent} from '../error-list/error-list.component';
import {NotifierService} from 'angular-notifier';
import {notificationType, warningMessage} from '../../PrecinctHelper';

@Component({
  selector: 'app-info-sidenav',
  templateUrl: './info-sidenav.component.html',
  styleUrls: ['./info-sidenav.component.css']
})
export class InfoSidenavComponent implements OnInit {
  @ViewChild(MatSidenav)
  public sidenav: MatSidenav;
  populationData: PopulationData;
  presidentialData: ElectionData[];
  electionData: ElectionData[];
  precinctID: string;
  errorList: ErrorListComponent;
  congressionalData: {};
  Number = Number;

  populationLabels = {
    total: 'Total',
    white: 'White',
    black: 'Black or African American',
    asian: 'Asian',
    pacificIslander: 'Native Hawaiian and Other Pacific Islander',
    hispanic: 'Hispanic',
    nativeAmerican: 'Native American',
    other: 'Others'
  };
  populationKeys = Object.keys(this.populationLabels);

  constructor(private http: HttpClient, private notifier: NotifierService) {
  }

  ngOnInit(): void {
  }

  addElectionData(electionData: ElectionData[]) {
    const congressionalData = electionData.filter(e => e.type.toString() === ElectionType[ElectionType.CONGRESSIONAL]);
    const congressionalDataDictionary = {};
    this.electionData = [];

    for (const candidate of congressionalData) {
      this.electionData.push(candidate);
      if (congressionalDataDictionary[candidate.year]) {
        congressionalDataDictionary[candidate.year].push(candidate);
      } else {
        congressionalDataDictionary[candidate.year] = [candidate];
      }
    }

    this.congressionalData = congressionalDataDictionary;
    this.presidentialData = electionData.filter(e => e.type.toString() === ElectionType[ElectionType.PRESIDENTIAL]);
    this.electionData = this.electionData.concat(this.presidentialData);
    this.sidenav.open();
  }

  commitElectionData() {
    if (!this.errorList.selectedError) {
      this.notifier.notify(notificationType, warningMessage);
      return;
    }
    this.http.post(`/datacorrection/editelectiondata?uid=${this.precinctID}&errID=${this.errorList.selectedError.id}`,
      JSON.stringify(this.electionData),
      {headers: new HttpHeaders({'Content-Type': 'application/json'})})
      .subscribe(() => this.errorList.selectedError.resolved = true);
  }

  commitPopulationData() {
    if (!this.errorList.selectedError) {
      this.notifier.notify(notificationType, warningMessage);
      return;
    }
    this.http.post(`/datacorrection/editpopulationdata?uid=${this.precinctID}&errID=${this.errorList.selectedError.id}`,
      JSON.stringify(this.populationData),
      {headers: new HttpHeaders({'Content-Type': 'application/json'})})
      .subscribe(() => this.errorList.selectedError.resolved = true);
  }
}
