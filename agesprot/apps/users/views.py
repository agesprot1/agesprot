# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import permission_required, login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic.list import ListView
from django.utils.encoding import force_bytes
from django.core.urlresolvers import reverse
from .forms import PasswordResetRequestForm
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.views.generic.edit import *
from django.core.mail import send_mail
from django.contrib import messages
from django.template import loader
from django.views.generic import *
from django.conf import settings
from .forms import *
import json

var_dir_template = 'users/'

class ResetPasswordRequestView(FormView):
	template_name = var_dir_template+'password_reset_email.html'
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
					'protocol': 'http',
				}
				subject_template_name = 'email/txt/password_reset_subject.txt'
				email_template_name = 'email/html/password_reset_subject.html'
				subject = 'Cambio de Contraseña'
				subject = ''.join(subject.splitlines())
				email_txt = loader.render_to_string(subject_template_name, data)
				email_html = loader.render_to_string(email_template_name, data)
				send_mail(subject, email_html, settings.DEFAULT_FROM_EMAIL, [user.email])
				result = self.form_valid(form)
				messages.success(request, 'Un correo ha sido enviado ha ' +user_email+". Por favor verifica tu correo y sigue las instrucciones.")
			except User.DoesNotExist:
				result = self.form_invalid(form)
				messages.warning(request, 'No hay una cuenta asociada con el correo electronico digitado.')
		return result

class PasswordResetConfirmView(FormView):
	template_name = var_dir_template+'password_reset_email.html'
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

class UserRegistrateView(FormView):
	template_name = var_dir_template+'registrate.html'
	form_class = UserForm
	success_url = reverse_lazy('registrate')

	def get_context_data(self, **kwargs):
		context = super(UserRegistrateView, self).get_context_data(**kwargs)
		context['title'] = 'Registrate en AgesProt'
		return context

	def form_valid(self, form):
		form.registrate_user()
		messages.success(self.request, "Registro exitoso")
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
		else:
			messages.error(request, "Error en la actualización")
		return HttpResponseRedirect(reverse_lazy(next_url))
	else:
		form = UserUpdateForm(instance = user)
	return render(request, var_dir_template+'update.html', {'forms': form, 'user_data': user_pk, 'next_url': next_url, 'title': 'Edición de usuarios'})

@permission_required('is_staff')
def change_state_user(request):
	user = request.GET.get('user')
	state = True if request.GET.get('state') == 'true' else False
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
	except User.DoesNotExist:
		response['type'] = 'error'
		response['status'] = '0'
		response['msg'] = 'Usuario no encontrado'
	return HttpResponse(json.dumps(response), "application/json")

@permission_required('is_staff')
def delete_user(request, user):
	response = {}
	try:
		user = User.objects.get(pk = user)
		user.delete()
		response['type'] = 'success'
		response['msg'] = 'Exito al eliminar el usuario'
	except User.DoesNotExist:
		response['type'] = 'error'
		response['msg'] = 'Usuario no encontrado'
	return HttpResponse(json.dumps(response), "application/json")