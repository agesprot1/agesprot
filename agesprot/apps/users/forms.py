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

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'is_superuser']
		widgets = {
			'first_name': TextInput(attrs = {'class': 'form-control', 'required': True}),
			'last_name': TextInput(attrs = {'class': 'form-control', 'required': True}),
			'email': EmailInput(attrs = {'class': 'form-control', 'required': True}),
		}
		labels = {
			'first_name': 'Nombres',
			'last_name': 'Apellidos',
			'email': 'Correo electrónico',
			'is_superuser': 'Usuario Administrador',
		}

class UserForm(forms.Form):
	first_name = forms.CharField(label = 'Nombres', widget = TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}))
	last_name = forms.CharField(label = 'Apellidos', widget = TextInput(attrs = {'class': 'form-control', 'maxlength': '30', 'required': True}))
	foto = forms.ImageField(label = 'Foto', required = False)
	email = forms.EmailField(label = 'Correo electrónico', widget = forms.EmailInput(attrs = {'class': 'form-control', 'required': True}))
	password = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'minlength': 8, 'required': False}))
	re_password = forms.CharField(label = 'Confirme contraseña', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'minlength': 8, 'required': True}))
	#type_user = forms.ChoiceField(label = 'Tipo de usuario', choices = [('0', 'Normal'), ('1', 'Administrador')], widget = Select(attrs = {'required': False, 'class': 'form-control'}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if User.objects.filter(email = email).exists():
			raise forms.ValidationError('El email ya se ecuentra en uso.')
		return email

	def clean_type_user(self):
		if self.cleaned_data.get('type_user').is_hidden:
			return '0'
		else:
			return self.cleaned_data.get('type_user')

	def clean_re_password(self):
		re_password = self.cleaned_data.get('re_password')
		password = self.cleaned_data.get('password')
		if password != re_password:
			raise forms.ValidationError('Las contraseñas no coinciden.')
		return re_password

	def save(self):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		username = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		email = self.cleaned_data.get('email')
		foto = self.cleaned_data.get('foto')
		type_user = self.cleaned_data.get('type_user')
		user = User.objects.create_user(username, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		profile = ProfileUser(user = user, foto = foto)
		profile.save()

class ChangePasswordForm(forms.Form):
	old_password = forms.CharField(label = 'Contraseña antigua', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'minlength': 8, 'required': True}))
	new_password = forms.CharField(label = 'Contraseña nueva', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'minlength': 8, 'required': True}))
	re_new_password = forms.CharField(label = 'Confirme la contraseña', widget = forms.PasswordInput(attrs = {'class': 'form-control', 'minlength': 8, 'required': True}))