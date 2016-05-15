from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from .views import *

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = patterns('agesprot.apps.users.views',
	url(r'^list_user/$', login_required(permission_required('is_staff')(UserListView.as_view())), name = 'list_user'),
	url(r'^registrate/$', login_forbidden(UserRegistrateView.as_view()), name = 'registrate'),
	url(r'^reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
	url(r'^reset_password', ResetPasswordRequestView.as_view(), name = "reset_password"),
	url(r'^change-state/$', 'change_state_user', name = 'change_state_user'),
	url(r'^response_message/$', TemplateView.as_view(template_name = 'users/response_message.html'), {'title': 'Bienvenido'}, name = 'response_message'),
)

urlpatterns += [
	url(r'^login/$', login_forbidden(auth_views.login), {'template_name': 'users/login.html', 'extra_context': {'title': 'Login'}}, name = 'login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/users/login'}, name = 'logout')
]