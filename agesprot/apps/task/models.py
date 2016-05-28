from __future__ import unicode_literals

from django.db import models
from agesprot.apps.base.models import Tipo_estado, Tipo_prioridad
from agesprot.apps.project.models import *

class Tarea(models.Model):
	nombre_tarea = models.CharField(max_length = 45)
	descripcion_tarea = models.CharField(max_length = 100)
	fecha_creacion = models.DateField(auto_now = True)
	fecha_entrega = models.DateField()
	estado = models.ForeignKey(Tipo_estado)
	prioridad = models.ForeignKey(Tipo_prioridad)
	proyecto = models.ForeignKey(Proyecto)

	def __str__(self):
		return self.nombre_tarea

	def __unicode__(self):
		return self.nombre_tarea

class Tarea_integrante(models.Model):
	role = models.ForeignKey(Roles_project)
	tarea = models.ForeignKey(Tarea)
