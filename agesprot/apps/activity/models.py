from __future__ import unicode_literals

from django.db import models
from agesprot.apps.project.models import *
from agesprot.apps.base.models import Tipo_estado, Tipo_prioridad

class Actividad(models.Model):
	nombre_actividad = models.CharField(max_length = 45)
	descripcion_actividad = models.CharField(max_length = 100)
	fecha_creacion = models.DateField(auto_now = True)
	fecha_entrega = models.DateField()
	estado = models.ForeignKey(Tipo_estado)
	prioridad = models.ForeignKey(Tipo_prioridad)
	proyecto = models.ForeignKey(Proyecto)

	def __str__(self):
		return self.nombre_actividad

	def __unicode__(self):
		return self.nombre_actividad

class Actividad_role(models.Model):
	role = models.ForeignKey(Roles_project)
	actividad = models.ForeignKey(Actividad)