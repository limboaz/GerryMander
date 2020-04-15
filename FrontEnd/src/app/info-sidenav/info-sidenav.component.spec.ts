import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoSidenavComponent } from './info-sidenav.component';

describe('InfoSidenavComponent', () => {
  let component: InfoSidenavComponent;
  let fixture: ComponentFixture<InfoSidenavComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InfoSidenavComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InfoSidenavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
