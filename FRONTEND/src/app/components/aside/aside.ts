import { Component } from '@angular/core';
import { Nav } from '../nav/nav';

@Component({
  selector: 'app-aside',
  standalone: true,
  imports: [Nav],
  templateUrl: './aside.html',
  styleUrl: './aside.css'
})
export class Aside {

}
