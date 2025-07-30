from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Agenda
from .serializers import AgendaSerializer
from ordenes.models import OrdenDeTrabajo  # Importamos el modelo de OT
from vehiculos.models import Vehiculo      # Importamos el modelo de Vehiculo
import datetime

class AgendaViewSet(viewsets.ModelViewSet):
    
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    # Endpoint: GET /api/agendas/{id}/disponibilidad/?dia=YYYY-MM-DD
    @action(detail=True, methods=['get'])
    def disponibilidad(self, request, pk=None):
        agenda = self.get_object()
        fecha_str = request.query_params.get('dia', None)

        if not fecha_str:
            return Response(
                {"error": "Debe proveer un día con el formato YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            dia_consulta = datetime.datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        horarios_disponibles = agenda.obtener_turnos_disponibles(dia_consulta)
        return Response({
            "dia": dia_consulta,
            "horarios_disponibles": horarios_disponibles
        })

    # Endpoint: POST /api/agendas/{id}/reservar_turno/
    @action(detail=True, methods=['post'])
    def reservar_turno(self, request, pk=None):
        agenda = self.get_object()
        
        # Obtenemos los datos del cuerpo de la petición POST
        fecha_hora_str = request.data.get('fecha_hora')
        vehiculo_id = request.data.get('vehiculo_id')

        if not fecha_hora_str or not vehiculo_id:
            return Response(
                {"error": "Se requiere 'fecha_hora' (YYYY-MM-DD HH:MM) y 'vehiculo_id'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            fecha_hora_reserva = datetime.datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        except (ValueError, Vehiculo.DoesNotExist) as e:
            return Response({"error": f"Datos inválidos: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # Usamos la lógica del modelo para verificar la disponibilidad
        if agenda.verificar_disponibilidad(fecha_hora_reserva):
            # Creamos la Orden de Trabajo para reservar el turno
            ot = OrdenDeTrabajo.objects.create(
                agenda=agenda,
                vehiculo=vehiculo,
                fecha_turno=fecha_hora_reserva,
                # Podés agregar otros campos por defecto aquí
            )
            return Response(
                {"mensaje": "Turno reservado exitosamente.", "orden_id": ot.id},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"error": "El horario seleccionado ya no está disponible."},
                status=status.HTTP_409_CONFLICT
            )