from django.db import models
import datetime

# Modelo para la configuración de la agenda de un Taller
class Agenda(models.Model):
    taller = models.OneToOneField(
        'talleres.Taller', 
        on_delete=models.CASCADE, 
        related_name='agenda'
    )
    
    # En lugar de una lista, usamos campos booleanos para los días laborales. Es más eficiente.
    lunes = models.BooleanField(default=True)
    martes = models.BooleanField(default=True)
    miercoles = models.BooleanField(default=True)
    jueves = models.BooleanField(default=True)
    viernes = models.BooleanField(default=True)
    sabado = models.BooleanField(default=False)
    domingo = models.BooleanField(default=False)

    horario_desde = models.TimeField()
    horario_hasta = models.TimeField()
    turnos_maximos_por_hora = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Agenda de {self.taller.nombre}"
    

        # --- NUEVOS MÉTODOS PARA LA LÓGICA DE TURNOS ---

    def verificar_disponibilidad(self, fecha_hora_propuesta):
        """
        Verifica si un slot de tiempo específico está disponible.
        """
        # 1. ¿El día de la semana se trabaja?
        dias_laborales = [self.lunes, self.martes, self.miercoles, self.jueves, self.viernes, self.sabado, self.domingo]
        if not dias_laborales[fecha_hora_propuesta.weekday()]:
            return False # No es un día laboral

        # 2. ¿La hora está dentro del horario laboral?
        if not (self.horario_desde <= fecha_hora_propuesta.time() < self.horario_hasta):
            return False # Fuera de horario

        # 3. ¿Hay lugar en esa franja horaria?
        turnos_en_esa_hora = self.ordenes.filter(fecha_turno__hour=fecha_hora_propuesta.hour).count()
        if turnos_en_esa_hora >= self.turnos_maximos_por_hora:
            return False # No hay más cupos en esta hora

        return True # ¡Hay lugar!

    def obtener_turnos_disponibles(self, dia):
        """
        Genera una lista de horarios disponibles para un día específico.
        """
        turnos_disponibles = []
        
        # Generar slots de una hora desde el inicio hasta el fin de la jornada
        hora_actual = datetime.datetime.combine(dia, self.horario_desde)
        hora_fin = datetime.datetime.combine(dia, self.horario_hasta)

        while hora_actual < hora_fin:
            # Usamos el método anterior para chequear cada slot
            if self.verificar_disponibilidad(hora_actual):
                turnos_disponibles.append(hora_actual.time())
            
            # Avanzamos a la siguiente hora
            hora_actual += datetime.timedelta(hours=1)
            
        return turnos_disponibles