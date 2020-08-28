from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import CurriculumForm
from alunos.models import Aluno
from empresas.models import Empresa

# Create your views here.
@login_required(login_url='login')
def job_list_view(request):
	job_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM vaga WHERE data_exp >= CURDATE()")
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
		cursor.execute("SELECT * FROM curriculo")
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
					'liberado': row[6],
				}

				curriculum_list.append(curriculum)

	context = {
		'curriculum_list': curriculum_list
	}

	return render(request, 'core/curriculum/list.html', context)

@login_required(login_url='login')
def curriculum_read_view(request, id=0):
	if id != 0:
		if request.method == 'POST':
			form = CurriculumForm(request.POST)

			if form.is_valid():
				data = form.clean_form()

				if data['liberado'] == 'sim':
					status_liberado = True
				else:
					status_liberado = False

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
							
						update_student.save()
					except:
						return redirect('/curriculos/')
		
				with connection.cursor() as cursor:
					instituicao = data['instituicao_ensino']
					curso = data['curso_extra']
					empresa = data['empresa']
					cargo = data['cargo']
					
					cursor.execute(
						"UPDATE curriculo SET instituicao_ensino=%s, curso_extra=%s, empresa=%s, cargo=%s, liberado=%s WHERE id=%s", 
						[instituicao, curso, empresa, cargo, status_liberado, id]
					)

					return redirect('/curriculos/')
			else:
				curriculum = request.POST

		else:
			with connection.cursor() as cursor:
				cursor.execute("SELECT * FROM curriculo WHERE id=%s", [id])
				result = cursor.fetchone()

				if result != None:
					try:
						student = Aluno.objects.get(id=result[1])
						curriculum = {
							'id': result[0],
							'nome': student.nome,
							'email': student.email,
							'instituicao_ensino': result[2],
							'curso_extra': result[3],
							'empresa': result[4],
							'cargo': result[5],
							'liberado': result[6],
						}
					except:
						return redirect('/curriculos/')
				else:
					return redirect('/curriculos/')
		
		context = {
			'curriculum': curriculum
		}

		return render(request, 'core/curriculum/read.html', context)
	else:
		return redirect('/curriculos/')

@login_required(login_url='login')
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