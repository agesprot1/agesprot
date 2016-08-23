from .models import *

def register_notification(request, user, icon, titulo_notificacion):
	notification = NotificationUser(user = user, icon = icon, titulo_notificacion = titulo_notificacion)
	notification.save()