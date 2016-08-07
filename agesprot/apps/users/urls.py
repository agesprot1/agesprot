from django.contrib.auth.decorators import permission_required, user_passes_test, login_required
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from .views import *

login_forbidden = user_passes_test(lambda u: u.is_anonymous(), '/project/my-list-project/')

urlpatterns = patterns('agesprot.apps.users.views',
	url(r'^list-user/$', permission_required('is_superuser')(UserListView.as_view()), name = 'list_user'),
	url(r'^change-state/$', 'change_state_user', name = 'change_state_user'),
	url(r'^delete-user/(?P<user>\d+)/$', 'delete_user', name = 'delete_user'),
	url(r'^update-user/(?P<user_pk>\d+)/$', 'update_user', name = "update_user"),
	url(r'^registrate/$', login_forbidden(UserRegistrateView.as_view()), name = 'registrate'),
	url(r'^reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(),name='reset_password_confirm'),
	url(r'^reset-password', ResetPasswordRequestView.as_view(), name = "reset_password"),
	url(r'^change-password/$', 'change_password', name = 'change_password'),
	url(r'^user-profile/$', login_required(TemplateView.as_view(template_name = 'users/profile_user.html')), {'title': 'Mi perfil'}, name = 'profile'),
	url(r'^response-message/$', TemplateView.as_view(template_name = 'users/response_message.html'), {'title': 'Bienvenido'}, name = 'response_message'),
	url(r'^update-foto/(?P<pk>\d+)/$', login_required(UpdateFotoUserView.as_view()), name = 'update_foto'),
	url(r'^logout/$', 'logout_user', name = 'logout')
)

urlpatterns += [
	url(r'^login/$', login_forbidden(auth_views.login), {'template_name': 'users/form_login.html', 'extra_context': {'title': 'Login'}}, name = 'login'),
	#url(r'^logout/$', auth_views.logout, {'next_page': '/users/login'}, name = 'logout')
]