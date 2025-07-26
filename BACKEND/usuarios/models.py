# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    # Definimos los roles que puede tener un usuario
    class Role(models.TextChoices):
        CLIENTE = "CLIENTE", "Cliente"
        ADMIN_TECNICO = "ADMIN_TECNICO", "Admin/Tecnico"
        SUPERUSUARIO = "SUPERUSUARIO", "Superusuario"

    # Campo base para el rol, con un valor por defecto
    base_role = Role.CLIENTE 

    # Campo para almacenar el rol específico del usuario
    role = models.CharField(max_length=50, choices=Role.choices)

    # Agregamos los campos del UML
    # 'nombre' y 'apellido' ya vienen en AbstractUser como 'first_name' y 'last_name'
    # 'mail' ya viene como 'email'
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Asignamos el rol por defecto si no se especifica uno
        if not self.pk:
            self.role = self.base_role
        return super().save(*args, **kwargs)