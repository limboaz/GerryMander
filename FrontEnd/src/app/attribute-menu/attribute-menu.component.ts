import {Component, Inject, OnInit, ViewChild} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {loadRequest} from '../../PrecinctHelper';
import {Correction} from '../../models/models';
import {MAT_DIALOG_DATA, MatDialog, MatDialogRef} from '@angular/material/dialog';
import {CorrectionType} from '../../models/enums';
import {MatTableDataSource} from '@angular/material/table';
import {MatPaginator} from '@angular/material/paginator';

const themeStyles = {
  'indigo-pink.css': '.sidenav-forms {background-color: #65B9CA;} .map-edit-buttons {background-color: #65B9CA;}',
  'deeppurple-amber.css': '.sidenav-forms {background-color: #65B9CA;} .map-edit-buttons {background-color: #65B9CA;}',
  'pink-bluegrey.css': 'a {color: #dabb13;} .sidenav-forms {background-color: #b33163;} .map-edit-buttons {background-color: #ff4294;}',
  'purple-green.css': 'a {color: #dabb13;} .sidenav-forms {background-color: #b33163;} .map-edit-buttons {background-color: #ff4294;}'
};

@Component({
  selector: 'app-attribute-menu',
  templateUrl: './attribute-menu.component.html',
  styleUrls: ['./attribute-menu.component.css']
})
export class AttributeMenuComponent implements OnInit {

  constructor(private http: HttpClient, public dialog: MatDialog) {
    this.changeTheme('deeppurple-amber.css');
  }

  ngOnInit(): void {
  }

  changeTheme(themeName) {
    // @ts-ignore
    document.getElementById('themeAsset').href = `assets/${themeName}`;
    const themeStyle = document.getElementById('themeStyle');
    themeStyle.innerHTML = '';
    themeStyle.appendChild(document.createTextNode(themeStyles[themeName]));
  }

  viewCorrectionsLog() {
    loadRequest(this.http.get('/data/getcorrectionlog'), (e: Correction[]) => {
      const dialogRef = this.dialog.open(CorrectionsLogComponent, {
        data: e
      });
    });
  }
}

@Component({
  selector: 'app-corrections-log',
  templateUrl: 'corrections-log.component.html',
})
export class CorrectionsLogComponent {
  CorrectionType = CorrectionType;

  public dataSource: MatTableDataSource<Correction>;
  @ViewChild(MatPaginator, {static: true}) paginator: MatPaginator;

  constructor(public dialogRef: MatDialogRef<CorrectionsLogComponent>, @Inject(MAT_DIALOG_DATA) public corrections: Correction[]) {
    this.dataSource = new MatTableDataSource<Correction>(corrections);
    this.dataSource.paginator = this.paginator;
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

}
