# -*- encoding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json

def data_paginate(request):
	response = {}
	count = 0
	notification = Paginator(NotificationUser.objects.filter(user = request.user.pk).order_by('-pk'), 10)
	notification = notification.page(request.GET.get('page')) if request.GET.get('page') else notification.page(1)
	for notification in NotificationUser.objects.filter(user = request.user.pk)[:5]:
		response[count] = {}
		response[count]['titulo_notificacion'] = notification.titulo_notificacion
		response[count]['fecha_notificacion'] = u''.join(naturaltime(notification.fecha_notificacion))
		response[count]['icon'] = notification.icon
		count += 1
	return HttpResponse(json.dumps(response), "application/json")

def notification_user(request):
	response = {}
	count = 0
	for notification in NotificationUser.objects.filter(user = request.user.pk).order_by('-pk')[:5]:
		response[count] = {}
		response[count]['titulo_notificacion'] = notification.titulo_notificacion
		response[count]['fecha_notificacion'] = u''.join(naturaltime(notification.fecha_notificacion))
		response[count]['icon'] = notification.icon
		count += 1
	return HttpResponse(json.dumps(response), "application/json")