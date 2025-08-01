from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models.agendas import Agenda
from .serializers import AgendaSerializer
from usuarios.models.admin_tecnico import AdministradorTecnico
from vehiculos.models.vehiculo import Vehiculo
from ordenes.serializers import OrdenDeTrabajoSerializer
import datetime

class AgendaViewSet(viewsets.ModelViewSet):
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
    # 👇 --- 1. OMITIMOS LA AUTENTICACIÓN POR AHORA ---
    # Dejamos el acceso abierto para poder probar sin tokens.
    permission_classes = [permissions.AllowAny] 

    @action(detail=True, methods=['get'], url_path='turnos-asignados')
    def turnos_asignados(self, request, pk=None):
        """
        Endpoint para ver los turnos (OTs) asignados a esta agenda.
        """
        agenda = self.get_object()
        turnos = agenda.get_turnos_asignados()
        serializer = OrdenDeTrabajoSerializer(turnos, many=True)
        return Response(serializer.data)

    # @action(detail=True, methods=['post'], url_path='reservar-turno')
    # def reservar_turno(self, request, pk=None):
    #     """
    #     Endpoint para reservar un turno.
    #     """
    #     agenda = self.get_object()
        
    #     # 👇 --- 2. SIMULAMOS EL USUARIO TÉCNICO ---
    #     # IMPORTANTE: Esto es solo para desarrollo.
    #     # Obtenemos el primer técnico de la base de datos para simular que está logueado.
    #     # Asegúrate de haber creado al menos un AdministradorTecnico en el panel de admin.
    #     tecnico = AdministradorTecnico.objects.first()
        
    #     if not tecnico:
    #         return Response(
    #             {"error": "No se encontró ningún Administrador Técnico en la base de datos para realizar la prueba."},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR
    #         )
    #     # --- FIN DE LA SIMULACIÓN ---

    #     try:
    #         # 1. Validamos la disponibilidad usando la lógica del modelo Agenda
    #         fecha_hora_str = request.data.get('fecha_hora')
    #         if not fecha_hora_str:
    #             raise ValueError("El campo 'fecha_hora' es requerido.")
            
    #         fecha_hora_reserva = datetime.datetime.strptime(fecha_hora_str, '%Y-%m-%d %H:%M')
    #         agenda.verificar_disponibilidad(fecha_hora_reserva)

    #         # 2. Obtenemos el vehículo
    #         vehiculo_id = request.data.get('vehiculo_id')
    #         if not vehiculo_id:
    #             raise ValueError("El campo 'vehiculo_id' es requerido.")
    #         vehiculo = Vehiculo.objects.get(id=vehiculo_id)

    #         # 3. Llamamos al método del modelo AdministradorTecnico para crear la OT
    #         orden = tecnico.crear_orden_de_trabajo(
    #             vehiculo=vehiculo,
    #             datos_adicionales=request.data
    #         )
            
    #         # 4. Actualizamos la orden recién creada con la agenda y la fecha del turno
    #         orden.agenda = agenda
    #         orden.fecha_turno = fecha_hora_reserva
    #         orden.save()

    #         serializer = OrdenDeTrabajoSerializer(orden)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     except (ValueError, Vehiculo.DoesNotExist) as e:
    #         # Capturamos errores de validación (disponibilidad, datos, etc.)
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    #     except Exception as e:
    #         # Capturamos cualquier otro error inesperado
    #         return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
