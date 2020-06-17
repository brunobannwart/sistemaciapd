from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Vaga
from .forms import VagaForm, VagaEditForm

# Create your views here.
@login_required(login_url='login')
def job_list_view(request):
	job_list = Vaga.objects.filter(email=request.user.email)
	context = {
		'job_list': job_list
	}
	return render(request, 'job/list.html', context)

@login_required(login_url='login')
def job_form_view(request, id=0): 
	if request.method == 'POST':
		if id == 0:
			form = VagaForm(request.POST, request.FILES)
		else:
			form = VagaEditForm(request.POST, request.FILES or None)

		if form.is_valid():
			data = form.clean_form()
						
			if id == 0:
				try:
					company_name = request.user.razao_social
					company_email = request.user.email
					create_job = Vaga.objects.create(razao_social=company_name, email=company_email, arquivo=data['arquivo'], 
									titulo=data['titulo'], data_exp=data['data_exp'], descricao=data['descricao'])
					create_event.save()
				finally:
					form = VagaForm()
					error = None
					return redirect('/vagas/')
			else:
				try:
					update_job = Vaga.objects.get(id=id)

					if request.FILES.get('arquivo', False):
						update_job.arquivo = data['arquivo']

					update_job.titulo = data['titulo']
					update_job.data_exp = data['data_exp']
					update_job.descricao = data['descricao']
					update_job.save()

				finally:
					form = VagaForm()
					error = None
					return redirect('/vagas/')
		else:
			job = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = VagaForm()
		error = None

		if id == 0:
			job = {
				'arquivo': None,
				'titulo': '',
				'data_exp': '',
				'descricao': '',
			}
		else:
			try:
				job = Vaga.objects.get(id=id)
			except:
				return redirect('/vagas/')

	context = {
		'job': job,
		'error': error
	} 
	return render(request, 'job/form.html', context)

@login_required(login_url='login')
def job_delete_view(request, id=0):
	try:
		job = Vaga.objects.get(id=id)
		job.delete()
	finally:
		return redirect('/vagas/')