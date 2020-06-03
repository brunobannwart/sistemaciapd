# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.
@login_required(login_url='login')
def course_list_view(request):
	course_list = []

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM curso")
		results = cursor.fetchall()

		for row in results:
			course = {
				'id': row[0],
				'arquivo': row[1],
				'titulo': row[2],
				'data_exp': row[3],
				'descricao': row[4],
			}

			course_list.append(course)

	context = {
		'course_list': course_list
	}
	return render(request, 'options/course/list.html', context)

@login_required(login_url='login')
def course_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM curso WHERE id=%s", [id]) 
			result = cursor.fetchone()

			if result != None:
				course = {
					'id': result[0],
					'arquivo': result[1],
					'titulo': result[2],
					'data_exp': result[3],
					'descricao': result[4],
				}

				context = {
					'course': course
				}

				return render(request, 'options/course/item.html', context)
			else:
				return redirect('/cursos/')
	else:
		return redirect('/cursos/')

@login_required(login_url='login')
def event_list_view(request):
	event_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM evento")
		results = cursor.fetchall()

		for row in results:
			event = {
				'id': row[0],
				'arquivo': row[1],
				'titulo': row[2],
				'data_exp': row[3],
				'descricao': row[4],
			}

			event_list.append(event)

	context = {
		'event_list': event_list
	}
	return render(request, 'options/event/list.html', context)

@login_required(login_url='login')
def event_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM evento WHERE id=%s", [id]) 
			result = cursor.fetchone()

			if result != None:
				event = {
					'id': result[0],
					'arquivo': result[1],
					'titulo': result[2],
					'data_exp': result[3],
					'descricao': result[4],
				}

				context = {
					'event': event
				}

				return render(request, 'options/event/item.html', context)
			else:
				return redirect('/eventos/')
	else:
		return redirect('/eventos/')

@login_required(login_url='login')
def game_list_view(request):
	game_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM jogo")
		results = cursor.fetchall()
		
		for row in results:
			game = {
				'id': row[0],
				'arquivo': row[1],
				'titulo': row[2],
				'url': row[3],
				'descricao': row[4],
			}
			game_list.append(game)

	context = {
		'game_list': game_list
	}
	return render(request, 'options/game/list.html', context)

@login_required(login_url='login')
def game_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM jogo WHERE id=%s", [id]) 
			result = cursor.fetchone()

			if result != None:
				game = {
					'id': result[0],
					'arquivo': result[1],
					'titulo': result[2],
					'url': result[3],
					'descricao': result[4],
				}

				context = {
					'game': game
				}

				return render(request, 'options/game/item.html', context)
			else:
				return redirect('/jogos/')
	else:
		return redirect('/jogos/')

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

	return render(request, 'options/job/list.html', context)

@login_required(login_url='login')
def job_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM vaga WHERE id=%s", [id]) 
			result = cursor.fetchone()

			if result != None:
				job = {
					'id': result[0],
					'arquivo': result[1],
					'titulo': result[2],
					'data_exp': result[3],
					'descricao': result[4],
				}

				context = {
					'job': job
				}

				return render(request, 'options/job/item.html', context)
			else:
				return redirect('/vagas/')
	else:
		return redirect('/vagas/')

@login_required(login_url='login')
def videolesson_list_view(request):
	videolesson_list = []

	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM videoaula")
		results = cursor.fetchall()
		
		for row in results:
			videolesson = {
				'id': row[0],
				'arquivo': row[1],
				'titulo': row[2],
				'url': row[3],
				'descricao': row[4],
			}
			videolesson_list.append(videolesson)

	context = {
		'videolesson_list': videolesson_list
	}

	return render(request, 'options/videolesson/list.html', context)

@login_required(login_url='login')
def videolesson_view(request, id=0):
	if id != 0:
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM videoaula WHERE id=%s", [id]) 
			result = cursor.fetchone()

			if result != None:
				videolesson = {
					'id': result[0],
					'arquivo': result[1],
					'titulo': result[2],
					'url': result[3],
					'descricao': result[4],
				}

				context = {
					'videolesson': videolesson
				}

				return render(request, 'options/videolesson/item.html', context)
			else:
				return redirect('/videoaulas/')
	else:
		return redirect('/videoaulas/')
