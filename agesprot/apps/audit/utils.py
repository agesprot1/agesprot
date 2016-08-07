# -*- encoding: utf-8 -*-
from .models import *

def register_activity_profile_user(user, descripcion):
	audit_user = AuditProfileUser(user = user, descripcion = descripcion)
	audit_user.save()

def register_activity_project(user, project, descripcion):
	audit_project = AuditProject(user = user, project = project, descripcion = descripcion)
	audit_project.save()