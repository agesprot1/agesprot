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

class RegistrateForm(forms.Form):
	email = forms.EmailField(label = 'Correo electrónico', widget = forms.EmailInput(attrs = {'class': 'form-control', 'required': True}))
	password = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'minlength': 8, 'required': True}))
	first_name = forms.CharField(label = 'Nombres', widget = TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}))
	last_name = forms.CharField(label = 'Apellidos', widget = TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}))
	foto = forms.FileField(label = 'Foto', required = False)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).exists():
			raise forms.ValidationError('El email ya se ecuentra en uso.')
		return email

	def registrate_user(self):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		username = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		email = self.cleaned_data.get('email')
		foto = self.cleaned_data.get('foto')
		user = User.objects.create_user(username, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		profile = ProfileUser(user = user, foto = foto)
		profile.save()