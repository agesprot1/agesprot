# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from agesprot.apps.project.models import Proyecto
from agesprot.apps.users.models import ProfileUser

class AuditProfileUser(models.Model):
	user = models.ForeignKey(User)
	descripcion = models.CharField(max_length = 300)
	fecha_auditoria = models.DateTimeField(auto_now = True)

class AuditProject(models.Model):
	user = models.ForeignKey(User)
	project = models.ForeignKey(Proyecto)
	descripcion = models.CharField(max_length = 300)
	fecha_auditoria = models.DateTimeField(auto_now = True)