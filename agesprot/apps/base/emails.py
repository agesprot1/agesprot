# -*- encoding: utf-8 -*-
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from mail_templated import send_mail
from django.conf import settings

def app_send_email(user, request, title, template, args):
	data = {
		'email': user.email,
		'domain': request,
		'site_name': 'AgesProt',
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'user': user,
		'token': default_token_generator.make_token(user),
		'protocol': 'http://',
		'subject': title,
		'args': args
	}
	email_template_name = template
	send_mail(email_template_name, data, settings.DEFAULT_FROM_EMAIL, [user.email])

def app_send_email_invitate(email, request, title, template, args):
	data = {
		'domain': request,
		'site_name': 'AgesProt',
		'protocol': 'http://',
		'subject': title,
		'args': args
	}
	email_template_name = template
	send_mail(email_template_name, data, settings.DEFAULT_FROM_EMAIL, [email])