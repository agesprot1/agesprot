from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class ProfileUser(models.Model):
	user = models.OneToOneField(User, primary_key = True)
	foto = models.ImageField(upload_to = 'img/users/', blank = True, null = True)

	def __str__(self):
		return str(self.user)

	def get_foto(self):
		if self.foto and hasattr(self.foto, 'url'):
			return self.foto.url
		else:
			return '/static/img/none.png'