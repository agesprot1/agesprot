from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class Tipo_estadoManager(models.Manager):
	def crear_tipo_estado(self, nombre_estado):
		estado = ''
		try:
			self.get(nombre_estado = nombre_estado)
		except ObjectDoesNotExist:
			estado = self.create(nombre_estado = nombre_estado)
		return estado

class Tipo_estado(models.Model):
	nombre_estado = models.CharField(max_length = 45)
	objects = Tipo_estadoManager()

	def __str__(self):
		return self.nombre_estado

	def __unicode__(self):
		return self.nombre_estado

class Tipo_prioridad(models.Model):
	nombre_prioridad = models.CharField(max_length = 45)
	color_prioridad = models.CharField(max_length = 15)

	def __str__(self):
		return self.nombre_prioridad

	def __unicode__(self):
		return self.nombre_prioridad

class Tipo_roleManager(models.Manager):
	def crear_tipo_role(self, nombre_role):
		role = ''
		try:
			self.get(nombre_role = nombre_role)
		except ObjectDoesNotExist:
			role = self.create(nombre_role = nombre_role)
		return role

class Tipo_role(models.Model):
	nombre_role = models.CharField(max_length = 45)
	objects = Tipo_roleManager()

	def __str__(self):
		return self.nombre_role

	def __unicode__(self):
		return self.nombre_role

estado = Tipo_estado.objects.crear_tipo_estado("Activo")
estado = Tipo_estado.objects.crear_tipo_estado("Inactivo")
estado = Tipo_estado.objects.crear_tipo_estado("Proceso")
estado = Tipo_estado.objects.crear_tipo_estado("Pendiente")
estado = Tipo_estado.objects.crear_tipo_estado("Terminado")
role = Tipo_role.objects.crear_tipo_role("Administrador")