import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {LayoutModule} from '@angular/cdk/layout';
import {MapComponent} from './map/map.component';
import {HttpClientModule} from '@angular/common/http';
import {AttributeMenuComponent} from './attribute-menu/attribute-menu.component';
import {MaterialModules} from './material.module';
import {InfoSidenavComponent} from './info-sidenav/info-sidenav.component';
import {ErrorListComponent} from './error-list/error-list.component';
import { DialogButtonComponent } from './dialog-button/dialog-button.component';
import {DialogButtonDialogComponent} from './dialog-button/dialog-button.component';
import {FormsModule} from '@angular/forms';


@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    AttributeMenuComponent,
    InfoSidenavComponent,
    ErrorListComponent,
    DialogButtonComponent,
    DialogButtonDialogComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    LayoutModule,
    HttpClientModule,
    MaterialModules
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
