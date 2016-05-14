from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.project.views',
	url(r'^new-project/$', NewProjectView.as_view(), name = 'new_project'),
)