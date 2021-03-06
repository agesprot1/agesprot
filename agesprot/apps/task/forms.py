# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from .models import *

class TareaForm(forms.ModelForm):
	class Meta:
		model = Tarea
		fields = '__all__'
		exclude = ('actividad', 'usuario', 'estado')
		widgets = {
			'nombre_tarea': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'descripcion_tarea': Textarea(attrs = {'rows': 5, 'class': 'form-control', 'maxlength': '100', 'required': True}),
			'fecha_entrega': TextInput(attrs = {'class': 'form-control date', 'required': True}),
		}
		labels = {
			'nombre_tarea': 'Nombre de la tarea',
			'descripcion_tarea': 'Descripción',
			'fecha_entrega': 'fecha de entrega',
		}

	def clean_prioridad(self):
		return Tipo_prioridad.objects.get(pk = self.cleaned_data.get('prioridad'))

	def __init__(self, *args, **kwargs):
		super(TareaForm, self).__init__(*args, **kwargs)
		self.fields['prioridad'] = forms.ChoiceField(label = "Prioridad", choices = [('', 'Seleccione un prioridad')]+[(x.pk, x.nombre_prioridad) for x in Tipo_prioridad.objects.all()], widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))

class ComentarioTareaForm(forms.ModelForm):
	class Meta:
		model = Comentario_tarea
		fields = '__all__'
		exclude = ('tarea', 'usuario', 'fecha_creacion')
		widgets = {
			'comentario': Textarea(attrs = {'rows': 3, 'class': 'form-control', 'maxlength': '300', 'required': True}),
		}

class DocumentoTareaForm(forms.ModelForm):
	class Meta:
		model = Documento
		fields = '__all__'
		exclude = ('tarea',)
		widgets = {
			'nombre_documento': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'documento': FileInput(attrs = {'required': True}),
		}
		labels = {
			'nombre_documento': 'Nombre del documento',
			'documento': 'Documento',
		}