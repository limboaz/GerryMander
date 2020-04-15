import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AttributeMenuComponent } from './attribute-menu.component';

describe('AttributeMenuComponent', () => {
  let component: AttributeMenuComponent;
  let fixture: ComponentFixture<AttributeMenuComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AttributeMenuComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AttributeMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
