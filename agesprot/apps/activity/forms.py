# -*- encoding: utf-8 -*-
from agesprot.apps.base.models import Tipo_estado, Tipo_prioridad
from django.forms import *
from django import forms
from .models import *

class ActivitieForm(forms.ModelForm):
	class Meta:
		model = Actividad
		fields = '__all__'
		exclude = ['proyecto']
		widgets = {
			'nombre_actividad': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'descripcion_actividad': Textarea(attrs = {'rows': 5, 'class': 'form-control', 'maxlength': '100', 'required': True}),
			'fecha_entrega': TextInput(attrs = {'class': 'form-control date', 'required': True}),
		}
		labels = {
			'nombre_proyecto': 'Nombre de la actividad',
			'descripcion_actividad': 'Descripción',
			'fecha_entrega': 'fecha_entrega',
		}

	def clean_estado(self):
		return Tipo_estado.objects.get(pk = self.cleaned_data.get('estado'))

	def clean_prioridad(self):
		return Tipo_prioridad.objects.get(pk = self.cleaned_data.get('prioridad'))

	def __init__(self, *args, **kwargs):
		super(ActivitieForm, self).__init__(*args, **kwargs)
		self.fields['estado'] = forms.ChoiceField(label = "Estado", choices = [('', 'Seleccione un estado')]+[(x.pk, x.nombre_estado) for x in Tipo_estado.objects.all()], widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))
		self.fields['prioridad'] = forms.ChoiceField(label = "Prioridad", choices = [('', 'Seleccione un prioridad')]+[(x.pk, x.nombre_prioridad) for x in Tipo_prioridad.objects.all()], widget = forms.Select(attrs = {'class': 'form-control', 'required': True}))