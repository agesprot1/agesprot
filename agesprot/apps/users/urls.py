from .views import *
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = patterns('agesprot.apps.users.views',
	#url(r'^registrate/$', login_forbidden(UserRegistrateView.as_view()), name = 'registrate'),
	url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
	url(r'^reset_password', ResetPasswordRequestView.as_view(), name = "reset_password"),
	url(r'^response_message/$', TemplateView.as_view(template_name = 'users/response_message.html'), {'title': 'Bienvenido'}, name = 'response_message'),
)

urlpatterns += [
	url(r'^login/$', login_forbidden(auth_views.login), {'template_name': 'users/login.html', 'extra_context': {'title': 'Login'}}, name = 'login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/users/login'}, name = 'logout')
]