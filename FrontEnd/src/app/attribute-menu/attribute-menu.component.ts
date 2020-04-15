import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-attribute-menu',
  templateUrl: './attribute-menu.component.html',
  styleUrls: ['./attribute-menu.component.css']
})
export class AttributeMenuComponent implements OnInit {
  demographicGroups: string[] = ['Black or African American', 'White', 'Asian', 'American Indian or Alaska Native', 'Hispanic',
    'Native Hawaiian or Other Pacific Islander'];

  constructor() {
  }

  ngOnInit(): void {
  }

}
