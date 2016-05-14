from __future__ import unicode_literals

from django.db import models
from agesprot.apps.base.models import Tipo_estado

class Proyecto(models.Model):
	nombre_proyecto = models.CharField(max_length = 45)
	descripcion = models.CharField(max_length = 200)
	fecha_inicio = models.DateField()
	fecha_final = models.DateField()
	estado = models.ForeignKey(Tipo_estado)

	def __str__(self):
		return self.nombre_proyecto