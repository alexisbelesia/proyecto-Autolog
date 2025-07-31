import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cli-turnos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cli-turnos.html',
  styleUrl: './cli-turnos.css'
})
export class CliTurnos {
  activeTab = signal<'turnos' | 'sugerido'>('turnos');

  setTab(tab: 'turnos' | 'sugerido') {
    this.activeTab.set(tab);
  }
}
