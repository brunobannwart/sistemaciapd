from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import CurriculumForm
from alunos.models import Aluno
from empresas.models import Empresa
import os

# Create your views here.
@login_required(login_url='login')
def job_list_view(request):
	job_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM vaga WHERE data_exp >= CURDATE() ORDER BY titulo ASC")
		results = cursor.fetchall()

		for row in results:
			try:
				company = Empresa.objects.get(id=row[1])
			except:
				company = None

			if company != None:
				job = {
					'id': row[0],
					'razao_social': company.razao_social,
					'email': company.email,
					'arquivo': settings.MEDIA_URL + row[2],
					'titulo': row[3],
					'data_exp': row[4],
					'descricao': row[5],
				}

				job_list.append(job)

	context = {
		'job_list': job_list
	}

	return render(request, 'core/job/list.html', context)

@login_required(login_url='login')
def job_read_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM vaga WHERE id=%s", [id])
			result = cursor.fetchone()

			if result != None:
				try:
					company = Empresa.objects.get(id=result[1])

					job = {
						'id': result[0],
						'razao_social': company.razao_social,
						'email': company.email,
						'arquivo': settings.MEDIA_URL + result[2],
						'titulo': result[3],
						'data_exp': result[4],
						'descricao': result[5],
					}

					context = {
						'job': job
					}

					return render(request, 'core/job/read.html', context)
				except:
					return redirect('/vagas/')
			else:
				return redirect('/vagas/')
	else:
		return redirect('/vagas/')

@login_required(login_url='login')
def curriculum_list_view(request):
	curriculum_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM curriculo ORDER BY created_at DESC")
		results = cursor.fetchall()
	
		for row in results:
			try:
				student = Aluno.objects.get(id=row[1])
			except:
				student = None

			if student != None:
				curriculum = {
					'id': row[0],
					'nome': student.nome,
					'email': student.email,
					'instituicao_ensino': row[2],
					'curso_extra': row[3],
					'empresa': row[4],
					'cargo': row[5],
					'laudo_medico': row[6],
					'liberado': row[7],
				}

				curriculum_list.append(curriculum)

	context = {
		'curriculum_list': curriculum_list
	}

	return render(request, 'core/curriculum/list.html', context)

@login_required(login_url='login')
@csrf_protect
def curriculum_read_view(request, id=0):
	if id != 0:
		if request.method == 'POST':
			form = CurriculumForm(request.POST, request.FILES or None)

			if form.is_valid():
				data = form.clean_form()

				if data['liberado'] == 'sim':
					status_liberado = True
				else:
					status_liberado = False

				if 'novo_laudo_medico' in request.FILES:
					file = request.FILES['novo_laudo_medico']
					filename = file.name
					
					filepath = 'curriculo/' + str(data['aluno_id']) + '/' + filename
					write = settings.MEDIA_ROOT + '/' + filepath

					with open(write, 'wb+') as destination:
						for chunk in file.chunks():
							destination.write(chunk)

					laudo_path = filepath

					if data['laudo_medico'] != '':
						if os.path.exists(settings.MEDIA_ROOT + '/' + data['laudo_medico']):
							os.remove(settings.MEDIA_ROOT + '/' + data['laudo_medico'])

				else:
					laudo_path = data['laudo_medico']

				if status_liberado:
					try:
						update_student = Aluno.objects.get(email=data['email'])

						if data['instituicao_ensino'] != '':
							update_student.instituicao_ensino = data['instituicao_ensino']

						if data['curso_extra'] != '':
							update_student.curso_extra = data['curso_extra']

						if data['empresa'] != '':
							update_student.empresa = data['empresa']

						if data['cargo'] != '':
							update_student.cargo = data['cargo']

						if laudo_path != '':	
							update_student.laudo_medico = laudo_path
							
						update_student.save()
					except:
						return redirect('/curriculos/')
		
				with connection.cursor() as cursor:
					instituicao = data['instituicao_ensino']
					curso = data['curso_extra']
					empresa = data['empresa']
					cargo = data['cargo']
					
					cursor.execute(
						"UPDATE curriculo SET instituicao_ensino=%s, curso_extra=%s, empresa=%s, cargo=%s, laudo_medico=%s, liberado=%s WHERE id=%s", 
						[instituicao, curso, empresa, cargo, laudo_path, status_liberado, id]
					)

				form = CurriculumForm()
				error = None
				return redirect('/curriculos/')
			else:
				curriculum = request.POST
				error = 'Alguns campos não foram preenchidos corretamente'

		else:
			form = CurriculumForm()
			error = None

			with connection.cursor() as cursor:
				cursor.execute("SELECT * FROM curriculo WHERE id=%s", [id])
				result = cursor.fetchone()

				if result != None:
					try:
						student = Aluno.objects.get(id=result[1])

						if result[6] != '':
							link_laudo = settings.MEDIA_URL + result[6]
						else:
							link_laudo = None

						curriculum = {
							'id': result[0],
							'aluno_id': result[1],
							'nome': student.nome,
							'email': student.email,
							'instituicao_ensino': result[2],
							'curso_extra': result[3],
							'empresa': result[4],
							'cargo': result[5],
							'laudo_medico': result[6],
							'link_laudo': link_laudo,
							'liberado': result[7],
						}
					except:
						return redirect('/curriculos/')
				else:
					return redirect('/curriculos/')
		
		context = {
			'curriculum': curriculum,
			'error': error
		}

		context.update(csrf(request))
		return render(request, 'core/curriculum/read.html', context)
	else:
		return redirect('/curriculos/')

@login_required(login_url='login')
@csrf_protect
def curriculum_delete_view(request, id=0):
	if request.method == 'POST':
		if id != 0:
			with connection.cursor() as cursor:
				cursor.execute("DELETE FROM curriculo WHERE id=%s", [id])

				return redirect('/curriculos/')
		else:
			return redirect('/curriculos/')
	else:
		return redirect('/curriculos/')