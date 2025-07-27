import { Routes } from '@angular/router';
import { Inicio } from './components/inicio/inicio'
import { Historial } from './components/historial/historial';

export const routes: Routes = [
    {path: '', component:Inicio},
    {path: 'historial/:vehiculoId', component: Historial}

];
