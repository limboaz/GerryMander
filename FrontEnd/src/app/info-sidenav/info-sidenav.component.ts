import {Component, OnInit, ViewChild} from '@angular/core';
import {MatSidenav} from '@angular/material/sidenav';
import {PopulationData, ElectionData} from '../../models/models';
import {CandidateParty, ElectionType} from '../../models/enums';

@Component({
  selector: 'app-info-sidenav',
  templateUrl: './info-sidenav.component.html',
  styleUrls: ['./info-sidenav.component.css']
})
export class InfoSidenavComponent implements OnInit {
  @ViewChild(MatSidenav)
  public sidenav: MatSidenav;

  CandidateParty = CandidateParty;
  populationData: PopulationData;
  presidentialData: ElectionData[];
  congressionalData;

  populationLabels = {
    total: 'Total',
    white: 'White',
    black: 'Black or African American',
    asian: 'Asian',
    pacificIslander: 'Native Hawaiian and Other Pacific Islander',
    hispanic: 'Hispanic',
    nativeAmerican: 'Native American',
    others: 'Others'
  };
  populationKeys = Object.keys(this.populationLabels);

  constructor() {}

  ngOnInit(): void {
  }

  addElectionData(electionData: ElectionData[]) {
    const congressionalData = electionData.filter(e => e.type.toString() === ElectionType[ElectionType.CONGRESSIONAL]);
    const congressionalDataDictionary = {};

    for (const candidate of congressionalData) {
      if (congressionalDataDictionary[candidate.year]) {
        congressionalDataDictionary[candidate.year].push(candidate);
      } else {
        congressionalDataDictionary[candidate.year] = [candidate];
      }
    }

    this.congressionalData = congressionalDataDictionary;
    this.presidentialData = electionData.filter(e => e.type.toString() === ElectionType[ElectionType.PRESIDENTIAL]);
    this.sidenav.open();
  }
}
