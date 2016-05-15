from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Role(models.Model):
	nombre_role = models.CharField(max_length = 45)

	def __str__(self):
		return self.nombre_role

class ProfileUser(models.Model):
	user = models.OneToOneField(User, primary_key = True)
	foto = models.ImageField(upload_to = 'img/users/', default = 'img/none.png', blank = True, null = True)

	def __str__(self):
		return str(self.user)