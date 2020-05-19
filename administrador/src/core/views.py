# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .forms import ChangePasswordForm
from administradores.models import Administrador
from alunos.models import Aluno

# Create your views here.
def changepassword_view(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)

		if form.is_valid():
			if form.cleaned_data.get('senha') == form.cleaned_data.get('confirma'):
				data = form.clean_form()
				
				if Administrador.objects.filter(email=data['email']):
					admin_change = Administrador.objects.get(email=data['email'])
					admin_change.senha = data['senha']
					admin_change.save()
					form = ChangePasswordForm()
					error = None
					return redirect('/administradores/')
				else:
					change = request.POST
					error = 'E-mail não cadastrado'	
			else:
				change = request.POST
				error = 'Senhas não conferem'
		else:
			change = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = ChangePasswordForm()

		change = {
			'email': '',
			'senha': '',
			'confirma': '',
		}

		error = None

	context = {
		'change': change,
		'error': error,
	}
	return render(request, 'core/administrator/password.html', context)

def job_list_view(request):
	job_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM vaga")
		results = cursor.fetchall()

		for row in results:
			job = {
				'id': row[0],
				'arquivo': row[1],
				'titulo': row[2],
				'data_exp': row[3],
				'descricao': row[4],
			}

			job_list.append(job)

	context = {
		'job_list': job_list
	}

	return render(request, 'core/job/list.html', context)

def job_read_view(request, id=0):
	if id != 0:
		job = None

		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM vaga WHERE id=%s", [id])
			result = cursor.fetchone()

			job = {
				'id': row[0],
				'arquivo': row[1],
				'titulo': row[2],
				'data_exp': row[3],
				'descricao': row[4],
			}

		context = {
			'job': job
		}

		return render(request, 'core/job/read.html', context)
	else:
		return redirect('/vagas/')

def curriculum_list_view(request):
	curriculum_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM curriculo")
		results = cursor.fetchall()
	
		for row in results:
			curriculum = {
				'id': row[0],
				'email': row[1],
				'intituicao_ensino': row[2],
				'curso_extra': row[3],
				'empresa': row[4],
				'cargo': row[5],
				'liberado': row[6],
			}

			curriculum_list.append(curriculum)

	context = {
		'curriculum_list': curriculum_list
	}

	return render(request, 'core/curriculum/list.html', context)

def curriculum_read_view(request, id=0):
	if id != 0:
		if request.method == 'POST':
			curriculum = None

			# with connection.cursor() as cursor:
			# 	cursor.execute("SELECT * FROM curriculo WHERE id=%s", [id])
			# 	result = cursor.fetchone()

			# 	curriculum_to_update = {
			# 		'id': result[0],
			# 		'email': result[1],
			# 		'intituicao_ensino': result[2],
			# 		'curso_extra': result[3],
			# 		'empresa': result[4],
			# 		'cargo': result[5],
			# 		'liberado': result[6],
			# 	}
			#
			#

		else:
			curriculum = None

			# with connection.cursor() as cursor:
			# 	cursor.execute("SELECT * FROM curriculo WHERE id=%s", [id])
			# 	result = cursor.fetchone()

			# 	curriculum = {
			# 		'id': result[0],
			# 		'email': result[1],
			# 		'intituicao_ensino': result[2],
			# 		'curso_extra': result[3],
			# 		'empresa': result[4],
			# 		'cargo': result[5],
			# 		'liberado': result[6],
			# 	}
		
			context = {
				'curriculum': curriculum
			}

			return render(request, 'core/curriculum/read.html', context)
	else:
		return redirect('/curriculos/')