# -*- encoding: utf-8 -*-
from .models import *

def register_activity_profile_user(user, descripcion):
	audit = AuditProfileUser(user = user, descripcion = descripcion)
	audit.save()