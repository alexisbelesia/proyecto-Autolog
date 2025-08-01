import { Component } from '@angular/core';

import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';


@Component({
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cli-talleres.html',
  styleUrl: './cli-talleres.css'
})
export class CliTalleres {
  constructor(private router: Router) {}

  pedirTurno() {
    this.router.navigate(['/cliente', 'pedir_turno']);
  }
}
