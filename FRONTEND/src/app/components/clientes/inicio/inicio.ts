import { Component, OnInit } from '@angular/core';
import { VehiculoService } from '../../../services/vehiculo/vehiculo.service'
import {Vehiculo} from '../../../models/vehiculo/vehiculo.model'

import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-inicio',
  imports: [CommonModule],
  templateUrl: './inicio.html',
  styleUrl: './inicio.css'
})
export class Inicio implements OnInit {
  vehiculos: Vehiculo[] = []
  
  constructor(private vehiculoService: VehiculoService) {}

  ngOnInit(): void {
    this.vehiculoService.getVehiculos().subscribe(data => this.vehiculos = data);
  }

  administrarPermisos(vehiculo: Vehiculo) {
    console.log(`Permisos para: ${vehiculo.patente}`);
  }

  verHistorial(vehiculo: Vehiculo) {
    console.log(`Historial de: ${vehiculo.patente}`);
  }


}
