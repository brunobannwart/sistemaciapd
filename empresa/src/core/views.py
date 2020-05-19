# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from .forms import ChangePasswordForm

# Create your views here.
def changepassword_view(request):
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)

		if form.is_valid():
			if form.cleaned_data.get('senha') == form.cleaned_data.get('confirma'):
				data = form.clean_form()
				form = ChangePasswordForm()
				error = None
				return redirect('/vagas/')
			else:
				change = request.POST
				error = 'Senhas não conferem'
		else:
			change = request.POST
			error = 'Alguns campos não foram preenchidos corretamente'
	else:
		form = ChangePasswordForm()
		error = None

		change = {
			'email': '',
			'senha': '',
			'confirma': ''
		}

	context = {
		'change': change,
		'error': error
	}

	return render(request, 'core/company/password.html', context)

def student_list_view(request):
	student_list = []
	
	with connection.cursor() as cursor:
		cursor.execute("SELECT * FROM aluno")
		results = cursor.fetchall()

		for row in results:
			student = {
				'id': row[0],
				'foto':	row[1],
				'nome': row[2],
				'data_nasc': row[3],
				'email': row[4],
				'cpf': row[6],
				'cep': row[8],
				'numero': row[9],
				'cid': row[10],
				'outra_info': row[14],
				'intituicao_ensino': row[15],
				'curso_extra': row[16],
				'empresa': row[17],
				'cargo': row[18],
			}
			student_list.append(student)
	
	context = {
		'student_list': student_list
	}

	return render(request, 'core/student/list.html', context)

def student_read_view(request, id=0):
	if id != 0:
		student = None
		
		with connection.cursor() as cursor:
			cursor.execute("SELECT * FROM aluno WHERE id= %s", [id])
			result = cursor.fetchone()

			student = {
				'id': result[0],
				'foto':	result[1],
				'nome': result[2],
				'data_nasc': result[3],
				'email': result[4],
				'cpf': result[6],
				'cep': result[8],
				'numero': result[9],
				'cid': result[10],
				'outra_info': result[14],
				'intituicao_ensino': row[15],
				'curso_extra': row[16],
				'empresa': row[17],
				'cargo': row[18],
			}
		
		context = {
			'student': student
		}

		return render(request, 'core/student/read.html', context)
	else:
		return redirect('/candidatos/')
