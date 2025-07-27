from django.db import models
from django.conf import settings
from talleres.models.taller import Taller

class AdministradorTecnico(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='administrador_tecnico'
    )
    taller = models.ForeignKey(
        Taller,
        on_delete=models.CASCADE,
        related_name='administradores_tecnicos'
    )

    def __str__(self):
        return f"Admin Técnico: {self.usuario.username} - Taller: {self.taller.nombre}"
