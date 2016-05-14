from .models import *
from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import ProjectForm

class NewProjectView(FormView):
	template_name = 'project/new_project.html'
	form_class = ProjectForm
	success_url = '/'

	def get_context_data(self, **kwargs):
		context = super(NewProjectView, self).get_context_data(**kwargs)
		context['title'] = 'Crear un nuevo projecto'
		return context