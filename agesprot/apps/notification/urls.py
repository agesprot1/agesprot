from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.notification.views',
	url(r'^$', 'notification_user', name = 'notification_user'),
	url(r'^data-paginate/$', 'data_paginate', name = 'data_paginate'),
	url(r'^me/$', login_required(TemplateView.as_view(template_name = 'notification/show.html')), {'title': 'Notificaciones'}, name = 'notification'),
)