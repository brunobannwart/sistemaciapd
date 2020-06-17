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
		cursor.execute("SELECT * FROM vaga WHERE data_exp >= CURDATE()")
		results = cursor.fetchall()

		for row in results:
			job = {
				'id': row[0],
				'razao_social': row[1],
				'email': row[2],
				'arquivo': row[3],
				'titulo': row[4],
				'data_exp': row[5],
				'descricao': row[6],
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
					'id': result[0],
					'razao_social': result[1],
					'email': result[2],
					'arquivo': result[3],
					'titulo': result[4],
					'data_exp': result[5],
					'descricao': result[6],
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
				'nome': row[1],
				'email': row[2],
				'instituicao_ensino': row[3],
				'curso_extra': row[4],
				'empresa': row[5],
				'cargo': row[6],
				'liberado': row[7],
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
						'nome': result[1],
						'email': result[2],
						'instituicao_ensino': result[3],
						'curso_extra': result[4],
						'empresa': result[5],
						'cargo': result[6],
						'liberado': result[7],
					}
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
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("DELETE FROM curriculo WHERE id=%s", [id])

			return redirect('/curriculos/')
	else:
		return redirect('/curriculos/')