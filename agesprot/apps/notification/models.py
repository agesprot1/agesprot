from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class NotificationUser(models.Model):
	user = models.ForeignKey(User)
	icon = models.CharField(max_length = 20, default = 'fa-tasks')
	titulo_notificacion = models.CharField(max_length = 500)
	fecha_notificacion = models.DateTimeField(auto_now = True)

	def __str__(self):
		return self.titulo_notificacion

	def __unicode__(self):
		return self.titulo_notificacion