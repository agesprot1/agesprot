from __future__ import unicode_literals

from django.db import models

class Tipo_estado(models.Model):
	nombre_estado = models.CharField(max_length = 45)

	def __str__(self):
		return self.nombre_estado

class Tipo_prioridad(models.Model):
	nombre_prioridad = models.CharField(max_length = 45)

	def __str__(self):
		return self.nombre_prioridad

class Tipo_role(models.Model):
	nombre_role = models.CharField(max_length = 45)

	def __str__(self):
		return self.nombre_role