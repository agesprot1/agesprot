from __future__ import unicode_literals

from django.db import models
from agesprot.apps.base.models import Tipo_estado

class Tipo_prioridad(models.Model):
	nombre_prioridad = models.CharField(max_length = 45)

	def __str__(self):
		return self.nombre_tarea

class Tarea(models.Model):
	nombre_tarea = models.CharField(max_length = 45)
	descripcion_tarea = models.CharField(max_length = 100)
	fecha_creacion = models.DateField(auto_now = True)
	fecha_entrega = models.DateField()
	estado = models.ForeignKey(Tipo_estado)
	prioridad = models.ForeignKey(Tipo_prioridad)

	def __str__(self):
		return self.nombre_tarea