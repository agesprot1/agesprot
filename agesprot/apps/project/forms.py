from django.forms import *
from django import forms
from .models import *

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Proyecto
		fields = '__all__'
		exclude = ('estado', )
		widgets = {
			'nombre_proyecto': TextInput(attrs = {'class': 'form-control', 'maxlength': '45', 'required': True}),
			'descripcion': TextInput(attrs = {'class': 'form-control', 'maxlength': '200', 'required': True}),
		}
		labels = {
			'nombre_proyecto': 'Nombre del proyecto',
			'descripcion': 'Descripcion del proyecto'
		}