from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection
from .forms import CurriculumForm
from alunos.models import Aluno

# Create your views here.
@login_required(login_url='login')
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

@login_required(login_url='login')
def job_read_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM vaga WHERE id=%s", [id])
			result = cursor.fetchone()

			if result != None:
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
	else:
		return redirect('/vagas/')

@login_required(login_url='login')
def curriculum_list_view(request):
	curriculum_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM curriculo")
		results = cursor.fetchall()
	
		for row in results:
			curriculum = {
				'id': row[0],
				'email': row[1],
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

						update_student.instituicao_ensino = data['instituicao_ensino']
						update_student.curso_extra = data['curso_extra']
						update_student.empresa = data['empresa']
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
					curriculum = {
						'id': result[0],
						'email': result[1],
						'instituicao_ensino': result[2],
						'curso_extra': result[3],
						'empresa': result[4],
						'cargo': result[5],
						'liberado': result[6],
					}
				else:
					return redirect('/curriculos/')
		
		context = {
			'curriculum': curriculum
		}

		return render(request, 'core/curriculum/read.html', context)
	else:
		return redirect('/curriculos/')