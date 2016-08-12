from django.core.management.base import BaseCommand
from agesprot.apps.base.models import *

class Command(BaseCommand):

	def handle(self, *args, **options):
		# Estados
		print "Creando estados....."
		Tipo_estado.objects.all().delete()
		Tipo_estado.objects.create(pk = 1, nombre_estado = "Activo")
		Tipo_estado.objects.create(pk = 2, nombre_estado = "Inactivo")
		Tipo_estado.objects.create(pk = 3, nombre_estado = "Proceso")
		Tipo_estado.objects.create(pk = 4, nombre_estado = "Pendiente")
		Tipo_estado.objects.create(pk = 5, nombre_estado = "Terminado")
		print "Exito al crear los estados"

		# Roles
		print "Creando roles....."
		Tipo_role.objects.all().delete()
		Tipo_role.objects.create(nombre_role = "Administrador")
		print "Exito al crear los roles"

		# Prioridades
		print "Creando priodidades....."
		Tipo_prioridad.objects.all().delete()
		Tipo_prioridad.objects.create(nombre_prioridad = "Alta", color_prioridad = "#c0392b")
		Tipo_prioridad.objects.create(nombre_prioridad = "Media", color_prioridad = "#d35400")
		Tipo_prioridad.objects.create(nombre_prioridad = "Baja", color_prioridad = "#2980b9")
		print "Exito al crear las prioridades"