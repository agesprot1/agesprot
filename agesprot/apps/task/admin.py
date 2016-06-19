from django.contrib import admin
from .models import *

admin.site.register(Tarea)
admin.site.register(Comentario_tarea)
admin.site.register(Documento)