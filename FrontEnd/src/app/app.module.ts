import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {MatSliderModule} from '@angular/material/slider';
import {MenuComponent} from './menu/menu.component';
import {LayoutModule} from '@angular/cdk/layout';
import {MapComponent} from './map/map.component';
import {HttpClientModule} from '@angular/common/http';
import {AttributeMenuComponent} from './attribute-menu/attribute-menu.component';
import {MaterialModules} from './material.module';


@NgModule({
  declarations: [
    AppComponent,
    MenuComponent,
    MapComponent,
    AttributeMenuComponent
  ],
  imports: [
    MatSliderModule,
    BrowserModule,
    BrowserAnimationsModule,
    LayoutModule,
    HttpClientModule,
    MaterialModules
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
