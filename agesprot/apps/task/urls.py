from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.task.views',
	url(r'^$', ListTaskProjectView.as_view(), name = 'all_task_project'),
	url(r'^new-task/$', NewTaskView.as_view(), name = 'new_task'),
)