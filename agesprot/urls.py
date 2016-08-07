from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('agesprot.apps.base.urls')),
	url(r'^users/', include('agesprot.apps.users.urls')),
	url(r'^project/', include('agesprot.apps.project.urls')),
	url(r'^notification/', include('agesprot.apps.notification.urls')),
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
