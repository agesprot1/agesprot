from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from agesprot.apps.base.models import Tipo_estado

class Project_role(models.Model):
	nombre_role = models.CharField(max_length = 45)

	def __str__(self):
		return self.nombre_role

class Proyecto(models.Model):
	nombre_proyecto = models.CharField(max_length = 45)
	descripcion = models.CharField(max_length = 200)
	fecha_inicio = models.DateField()
	fecha_final = models.DateField()
	estado = models.ForeignKey(Tipo_estado, default = 1)
	user = models.ForeignKey(User, blank = True, null = True)

	def __str__(self):
		return self.nombre_proyecto

	def __unicode__(self):
		return self.nombre_proyecto