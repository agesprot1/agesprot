from django.contrib.auth.decorators import login_required
from django.conf.urls import include, patterns, url
from .views import *

task_patterns = [
	url(r'^update-task/$', login_required(UpdateTaskActivityView.as_view()), name = 'update_task'),
	url(r'^delete-task/$', delete_task, name = 'delete_task'),
	url(r'^detail-task/$', login_required(DetailTaskView.as_view()), name = 'detail_task'),
	url(r'^create-comment-task/$', login_required(NewTaskCommentView.as_view()), name = 'create_comment_task'),
	url(r'^delete-comment/(?P<pk_comment>\d+)/$', delete_comment, name = 'delete_comment'),
	url(r'^upload-file/$', login_required(UploadFileView.as_view()), name = 'upload_file'),
	url(r'^delete-document/(?P<pk_document>\d+)/$', delete_document, name = 'delete_document'),
	url(r'^download-document/(?P<pk_document>\d+)/$', download_document, name = 'download_document'),
	url(r'^change-state/(?P<state>\d+)/$', change_state_task, name = 'change_state_task'),
]

urlpatterns = patterns('agesprot.apps.task.views',
	url(r'^add-task-activity/$', login_required(NewTaskActivityView.as_view()), name = 'add_task_activity'),
	url(r'^(?P<pk_task>\d+)/', include(task_patterns)),
)