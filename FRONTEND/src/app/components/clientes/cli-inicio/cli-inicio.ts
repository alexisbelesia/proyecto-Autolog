import { Component, OnInit } from '@angular/core';
import { VehiculoService } from '../../../services/vehiculo/vehiculo.service'
import {Vehiculo} from '../../../models/vehiculo/vehiculo.model'

import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cli-inicio.html',
  styleUrl: './cli-inicio.css'
})
export class CliInicio implements OnInit {
  vehiculos: Vehiculo[] = []
  
  constructor(private vehiculoService: VehiculoService, private router: Router) {}

  ngOnInit(): void {
    this.vehiculoService.getVehiculos().subscribe(data => this.vehiculos = data);
  }

  administrarPermisos(vehiculo: Vehiculo) {
    console.log(`Permisos para: ${vehiculo.patente}`);
  //  this.router.navigate(['/permisos']);
  }

  verHistorial(vehiculo: Vehiculo) {
    console.log(`Historial de: ${vehiculo.patente}`);
    this.router.navigate(['/cliente', 'historial', vehiculo.id]);
  }

  proximoMantenimiento(vehiculo: Vehiculo) {

  }

  kilometraje(vehiculo: Vehiculo) {
    
  }

}
