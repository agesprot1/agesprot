# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from agesprot.apps.audit.utils import register_activity_profile_user
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.core.urlresolvers import reverse
from .forms import PasswordResetRequestForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth import logout
from mail_templated import send_mail
from django.contrib import messages
from django.template import loader
from django.views.generic import *
from django.conf import settings
from .forms import *
import json

var_dir_template = 'users/'

class ResetPasswordRequestView(FormView):
	template_name = var_dir_template+'form_password_reset_email.html'
	success_url = reverse_lazy('response_message')
	form_class = PasswordResetRequestForm

	def get_context_data(self, **kwargs):
		context = super(ResetPasswordRequestView, self).get_context_data(**kwargs)
		context['title'] = 'Recuperación de cuenta'
		return context

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data["user_email"]
			try:
				user = User.objects.get(email = user_email)
				data = {
					'email': user.email,
					'domain': request.META['HTTP_HOST'],
					'site_name': 'AgesProt',
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'user': user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http://',
					'subject': 'Cambio de Contraseña'
				}
				register_activity_profile_user(user, 'Solicitud cambio de contraseña')
				#register_notification(user, 'fa fa-unlock', 'Solicitud Cambio de contraseña', '#')
				email_template_name = 'email/password_reset_subject.html'
				send_mail(email_template_name, data, settings.DEFAULT_FROM_EMAIL, [user.email])
				result = self.form_valid(form)
				messages.success(request, 'Un correo ha sido enviado ha ' +user_email+". Por favor verifica tu correo y sigue las instrucciones.")
			except User.DoesNotExist:
				result = self.form_invalid(form)
				messages.warning(request, 'No hay una cuenta asociada con el correo electronico digitado.')
		return result

class PasswordResetConfirmView(FormView):
	template_name = var_dir_template+'form_password_reset_email.html'
	success_url = reverse_lazy('response_message')
	form_class = SetPasswordForm

	def get_context_data(self, **kwargs):
		context = super(PasswordResetConfirmView, self).get_context_data(**kwargs)
		context['title'] = 'Recuperación de cuenta'
		return context

	@staticmethod
	def validate_url(uidb64, token):
		UserModel = get_user_model()
		assert uidb64 is not None and token is not None
		try:
			uid = urlsafe_base64_decode(uidb64)
			user = UserModel._default_manager.get(pk = uid)
		except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
			user = None
		return user

	def post(self, request, uidb64 = None, token = None, *arg, **kwargs):
		user = self.validate_url(uidb64, token)
		form = self.form_class(request.POST)
		if user is not None and default_token_generator.check_token(user, token):
			if form.is_valid():
				new_password = form.cleaned_data['new_password2']
				user.set_password(new_password)
				user.save()
				messages.success(request, 'Cambio de contraseña exitoso.')
				register_activity_profile_user(user, 'Cambio de contraseña realizado por solicitud')
				return self.form_valid(form)
			else:
				messages.warning(request, 'Ha ocurrido un error.')
				return self.form_invalid(form)
		else:
			messages.warning(request, 'La URL no es válida.')
			return HttpResponseRedirect(reverse('response_message'))

class UserListView(ListView):
	template_name = var_dir_template+'list_user.html'
	model = User

	def get_context_data(self, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)
		context['title'] = 'Lista de usuarios'
		return context

class UserRegistrateView(SuccessMessageMixin, FormView):
	template_name = var_dir_template+'form_registrate.html'
	success_message = 'Gracias por registrarse en AgesProt.'
	success_url = reverse_lazy('login')
	form_class = UserForm

	def get_context_data(self, **kwargs):
		context = super(UserRegistrateView, self).get_context_data(**kwargs)
		context['title'] = 'Registrate en AgesProt'
		return context

	def form_valid(self, form):
		form.save()
		return super(UserRegistrateView, self).form_valid(form)

@login_required
def update_user(request, user_pk):
	response = {}
	next_url = request.GET.get('next')
	user = get_object_or_404(User, pk = user_pk)
	if request.method == 'POST':
		form = UserUpdateForm(request.POST or None, request.FILES or None, instance = user)
		if form.is_valid():
			user_form = form.save(commit = False)
			user_form.username = user_form.email
			user_form.is_superuser = user_form.is_superuser if user_form.is_superuser != '' else user.is_superuser
			user_form.save()
			messages.success(request, "Exito en la actualización")
			register_activity_profile_user(request.user, 'Datos de usuario '+user.email+' actualzado')
		else:
			messages.error(request, "Error en la actualización")
		return HttpResponseRedirect(reverse_lazy(next_url))
	else:
		form = UserUpdateForm(instance = user)
	return render(request, var_dir_template+'form_update_user.html', {'forms': form, 'user_data': user_pk, 'next_url': next_url, 'title': 'Edición de usuarios'})

@permission_required('is_superuser')
def change_state_user(request):
	user = request.GET.get('user')
	state = True if request.GET.get('state') == 'true' else False
	state_text = "Activo" if state is True else "Inactivo"
	response = {}
	try:
		user = User.objects.get(pk = user)
		user.is_active = state
		user.save()
		response['type'] = 'success'
		response['status'] = '1'
		response['text'] = 'Activo'
		response['msg'] = 'Estado cambiado'
		response['state_label'] = 'false' if state is True else 'true'
		response['type_label'] = 'success' if state is True else 'danger'
		response['text_label'] = 'Activo' if state is True else 'Inactivo'
		register_activity_profile_user(request.user, 'Cambio de estado a '+state_text+' del usuario '+user.email)
	except User.DoesNotExist:
		response['type'] = 'error'
		response['status'] = '0'
		response['msg'] = 'Usuario no encontrado'
	return HttpResponse(json.dumps(response), "application/json")

@permission_required('is_superuser')
def delete_user(request, user):
	response = {}
	user = User.objects.get(pk = user)
	user.delete()
	response['type'] = 'success'
	response['msg'] = 'Exito al eliminar el usuario'
	register_activity_profile_user(request.user, 'Usuario '+user.email+' eliminado')
	return HttpResponse(json.dumps(response), "application/json")

@login_required
def change_password(request):
	if request.method == 'POST':
		response = {}
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			old_password = form.cleaned_data['old_password']
			new_password = form.cleaned_data['new_password']
			re_new_password = form.cleaned_data['re_new_password']
			if new_password == re_new_password:
				saveuser = User.objects.get(pk = request.user.pk)
				if request.user.check_password(old_password):
					saveuser.set_password(new_password);
					saveuser.save()
					response['type'] = 'success'
					response['msg'] = 'Cambio de contraseña exitoso.'
					register_activity_profile_user(request.user, 'Cambio de contraseña')
				else:
					response['type'] = 'error'
					response['msg'] = 'Contraseña antigua errónea.'
			else:
				response['type'] = 'error'
				response['msg'] = 'Contraseñas no coinciden.'
		return HttpResponse(json.dumps(response), "application/json")
	else:
		form = ChangePasswordForm()
	return render(request, var_dir_template+'form_password.html', {'forms': form, 'title': 'Cambiar mi contraseña'})

class UpdateFotoUserView(SuccessMessageMixin, UpdateView):
	template_name = var_dir_template+'form_foto_user.html'
	success_url = reverse_lazy('profile')
	success_message = 'Foto actualizada con exito.'
	form_class = ChangePhotoUserForm
	model = ProfileUser

	def get_context_data(self, **kwargs):
		context = super(UpdateFotoUserView, self).get_context_data(**kwargs)
		context['title'] = 'Actualizar foto'
		return context

	def form_valid(self, form):
		register_activity_profile_user(self.request.user, 'Actualización de foto')
		form.instance.user = self.request.user
		return super(UpdateFotoUserView, self).form_valid(form)

def logout_user(request):
	register_activity_profile_user(request.user, 'Salida de Agesprot')
	logout(request)
	return HttpResponseRedirect(reverse_lazy('login'))