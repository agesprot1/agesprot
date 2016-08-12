# -*- encoding: utf-8 -*-
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
import json

def data_paginate(request):
	response = {}
	count = 0
	data_notification = NotificationUser.objects.filter(user = request.user.pk).order_by('-pk')
	page_notification = Paginator(data_notification, (data_notification.count() / 5))
	try:
		page_notification = page_notification.page(request.GET.get('page'))
		response['type'] = 1
		response['data'] = {}
		for notification in page_notification:
			response['data'][count] = {}
			response['data'][count]['titulo_notificacion'] = notification.titulo_notificacion
			response['data'][count]['fecha_notificacion'] = u''.join(naturaltime(notification.fecha_notificacion))
			response['data'][count]['icon'] = notification.icon
			response['data'][count]['pk'] = str(notification.pk)
			count += 1
	except EmptyPage:
		response['type'] = 0
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