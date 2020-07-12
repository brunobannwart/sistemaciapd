from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Curso
from .forms import CursoForm, CursoEditForm

# Create your views here.
@login_required(login_url='login')
def course_list_view(request):
	course_list = Curso.objects.all()
	context = {
		'course_list': course_list
	}
	return render(request, 'course/list.html', context)

@login_required(login_url='login')
def course_form_view(request, id=0): 
	if request.method == 'POST':

		if id == 0:
			form = CursoForm(request.POST, request.FILES)
		else:
			form = CursoEditForm(request.POST, request.FILES or None)

		if form.is_valid():
			data = form.clean_form()
			
			if id == 0:
				try:
					create_course = Curso.objects.create(arquivo=data['arquivo'], titulo=data['titulo'], data_exp=data['data_exp'], descricao=data['descricao'])
					create_course.save()

				finally:
					form = CursoForm()
					error = None
					return redirect('/cursos/')
			else:
				try:
					update_course = Curso.objects.get(id=id)
				
					if request.FILES.get('arquivo', False):
						update_course.arquivo = data['arquivo']
				
					update_course.titulo = data['titulo']
					update_course.data_exp = data['data_exp']
					update_course.descricao = data['descricao']
					update_course.save()

				finally:
					form = CursoForm()
					error = None
					return redirect('/cursos/')
		else:
			course = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = CursoForm()
		error = None 

		if id == 0:
			course = {
				'arquivo': None,
				'titulo': '',
				'data_exp': '',
				'descricao': '',
				'url': '',
			}
		else:
			try:
				course = Curso.objects.get(id=id)
			except:
				return redirect('/cursos/')

	context = {
		'course': course,
		'error': error
	} 

	return render(request, 'course/form.html', context)

@login_required(login_url='login')
def course_delete_view(request, id=0):
	if request.method == 'POST':	
		try:
			course = Curso.objects.get(id=id)
			course.delete()
		finally:
			return redirect('/cursos/')
	else:
		return redirect('/cursos/')