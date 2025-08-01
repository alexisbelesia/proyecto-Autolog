import { Routes } from '@angular/router';

import { CliInicio } from './components/clientes/cli-inicio/cli-inicio';
import { Historial } from './components/clientes/cli-inicio/historial/historial';
import { CliTurnos } from './components/clientes/cli-turnos/cli-turnos';
import { CliTalleres } from './components/clientes/cli-talleres/cli-talleres';
import { CliPedirTurno} from './components/clientes/cli-talleres/cli-pedir_turno/cli-pedir_turno'
import { CliPm } from './components/clientes/cli-pm/cli-pm';
import { CliConfig } from './components/clientes/cli-config/cli-config';

import { TaOrdenes } from './components/talleres/ta-ordenes/ta-ordenes';
import { TaClientes } from './components/talleres/ta-clientes/ta-clientes';
import { TaVehiculos } from './components/talleres/ta-vehiculos/ta-vehiculos';
import { TaTurnos} from './components/talleres/ta-turnos/ta-turnos';
import { TaConfig } from './components/talleres/ta-config/ta-config';   

export const routes: Routes = [
    {path: 'cliente', component: CliInicio},
    {path: 'cliente/historial/:vehiculoId', component: Historial},
    {path: 'cliente/turnos', component: CliTurnos},
    {path: 'cliente/talleres', component: CliTalleres},
    {path: 'cliente/pedir_turno', component: CliPedirTurno},
    {path: 'cliente/pm', component: CliPm},
    {path: 'cliente/config', component: CliConfig},

    {path: 'taller/ordenes', component: TaOrdenes},
    {path: 'taller/clientes', component: TaClientes},
    {path: 'taller/vehiculos', component: TaVehiculos},
    {path: 'taller/turnos', component: TaTurnos},
    {path: 'taller/config', component: TaConfig}
];
