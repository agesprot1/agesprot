from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.task.views',
	url(r'^$', 'all_task_project', name = 'all_task_project'),
)