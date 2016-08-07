from __future__ import unicode_literals

from agesprot.apps.base.models import Tipo_estado, Tipo_prioridad
from django.contrib.contenttypes.models import ContentType
from agesprot.apps.activity.models import Actividad
from django.contrib.auth.models import User
from django.db import models

class Tarea(models.Model):
	nombre_tarea = models.CharField(max_length = 45)
	descripcion_tarea = models.CharField(max_length = 300)
	fecha_creacion = models.DateField(auto_now = True)
	fecha_entrega = models.DateField()
	estado = models.ForeignKey(Tipo_estado)
	prioridad = models.ForeignKey(Tipo_prioridad)
	actividad = models.ForeignKey(Actividad)
	usuario = models.ForeignKey(User)

	def __str__(self):
		return self.nombre_tarea

	def __unicode__(self):
		return self.nombre_tarea

class Comentario_tarea(models.Model):
	comentario = models.CharField(max_length = 300)
	fecha_creacion = models.DateField(auto_now = True, null = True, blank = True)
	tarea = models.ForeignKey(Tarea)
	usuario = models.ForeignKey(User)

	def __str__(self):
		return self.comentario

	def __unicode__(self):
		return self.comentario

def get_path(instance, filename):
	tarea = instance.tarea
	return 'file/project/'+str(tarea.actividad.proyecto.pk)+'/activities/'+str(tarea.actividad.pk)+'/task/'+str(tarea.pk)+'/'+filename

class Documento(models.Model):
	nombre_documento = models.CharField(max_length = 45)
	documento = models.FileField(upload_to = get_path)
	tarea = models.ForeignKey(Tarea)

	def __str__(self):
		return self.nombre_documento

	def __unicode__(self):
		return self.nombre_documento