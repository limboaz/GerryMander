import {Component, OnInit} from '@angular/core';

const themeStyles = {
  'indigo-pink.css': '',
  'deeppurple-amber.css': '',
  'pink-bluegrey.css': 'a {color: #dabb13;}',
  'purple-green.css': 'a {color: #dabb13;}'
};

@Component({
  selector: 'app-attribute-menu',
  templateUrl: './attribute-menu.component.html',
  styleUrls: ['./attribute-menu.component.css']
})
export class AttributeMenuComponent implements OnInit {
  constructor() {
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
}
