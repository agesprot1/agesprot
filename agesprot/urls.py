from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^', include('agesprot.apps.base.urls')),
	url(r'^users/', include('agesprot.apps.users.urls')),
	url(r'^project/', include('agesprot.apps.project.urls')),
]
