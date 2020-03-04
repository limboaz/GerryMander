import {Component, OnInit, Inject, EventEmitter, Output, Input} from '@angular/core';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';

export interface DialogData {
  name: string;
  field: any;
}

@Component({
  selector: 'app-dialog-button',
  templateUrl: './dialog-button.component.html',
  styleUrls: ['./dialog-button.component.css']
})
export class DialogButtonComponent implements OnInit {
  @Input() fieldName: string;
  @Input() fieldValue: any;
  @Output() valueChange = new EventEmitter();
  constructor(public dialog: MatDialog) { }

  ngOnInit(): void {
  }

  onClick() {
    const dialogRef = this.dialog.open(DialogButtonDialogComponent, {
      width: '250px',
      data: {name: this.fieldName, field: this.fieldValue}
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.fieldValue = result;
      this.valueChange.emit(this.fieldValue);
    });
  }

}

@Component({
  selector: 'app-dialog-button-dialog',
  templateUrl: './dialog-button-dialog.component.html'
})
export class DialogButtonDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<DialogButtonDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {

  }
  onNoClick(): void {
    this.dialogRef.close();
  }

}
