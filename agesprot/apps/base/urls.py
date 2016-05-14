from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.base.views',
	url(r'^$', login_required(TemplateView.as_view(template_name = 'home/index.html')), {'title': 'Bienvenido'}, name = 'home'),
)