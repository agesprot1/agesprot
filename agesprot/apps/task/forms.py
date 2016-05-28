# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from .models import *

class Tarea_form(forms.ModelForm):
	class Meta:
		model = Tarea
		fields = '__all__'
		exclude = ('proyecto', 'user')

	def __init__(self, *args, **kwargs):
		super(Tarea_form, self).__init__(*args, **kwargs)
		for name, field in self.fields.iteritems():
			field.widget.attrs['class'] = 'form-control'
			field.widget.attrs['required'] = 'required'