# -*- encoding: utf-8 -*-
from django.forms import *
from django import forms
from .models import *

class PasswordResetRequestForm(forms.Form):
	user_email = forms.CharField(label = 'Digite correo electrónico', widget = forms.EmailInput(attrs = {'class': 'form-control', 'required': True}))

class SetPasswordForm(forms.Form):
	error_messages = {
		'password_mismatch': ("Las contraseñas no coinciden."),
	}
	new_password1 = forms.CharField(label = ("Contraseña nueva"), widget=forms.PasswordInput(attrs = {'class': 'form-control', 'required': True}))
	new_password2 = forms.CharField(label = ("Confirme contraseña"), widget=forms.PasswordInput(attrs = {'class': 'form-control', 'required': True}))

	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password2')
		if password1 != password2:
			raise forms.ValidationError(self.error_messages['password_mismatch'], code = 'error')
		return password2