from django.contrib.auth.decorators import login_required
from django.conf.urls import include, patterns, url
from .views import *

urlpatterns = patterns('agesprot.apps.activity.views',
	url(r'^(?P<pk>\d+)/(?P<tag_url>.+)/$', login_required(ListActivitiesView.as_view()), name = 'list_activities'),
	url(r'^new-activity/(?P<pk>\d+)/$', login_required(NewActivitieView.as_view()), name = 'new_activities'),
	url(r'^update-activity/(?P<pk>\d+)/(?P<pk_project>\d+)/$', login_required(UpdateActivitieView.as_view()), name = 'update_activities'),
	url(r'^delete-activity/(?P<pk>\d+)/$', 'delete_activities', name = 'delete_activities'),
	url(r'^task/', include('agesprot.apps.task.urls')),
)