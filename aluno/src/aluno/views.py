#from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db import connection
import os, requests, io
from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image
from .forms import LoginForm
from .backend import LoginBackend
from core_aluno.models import LoginAluno

@csrf_protect
def login_view(request):
	if request.method == 'POST':
		try:
			form = LoginForm(request.POST)
		
			if form.is_valid():
				data = form.clean_form()
				login_student = LoginBackend.authenticate(request, data['email'], data['senha_hash'])

				if login_student != None and login_student != False:
					login_student.is_authenticated = True
					login_student.save()
					form = LoginForm()
					login(request, login_student, backend='aluno.backend.LoginBackend')
					return redirect('/inicio/')
				else:
					if login_student == False:
						login_form = request.POST
						error = 'Senha não confere'
					else:
						login_form = request.POST
						error = 'Não existe aluno com esse e-mail'
			else:
				login_form = request.POST
				error = 'Preencher campos de login corretamente'
		except:
			login_form = request.POST
			error = 'Não foi possível realizar o login. Tente novamente'
	else:
		form = LoginForm()
		error = None

		login_form = {
			'email': '',
			'senha': '',
		}

	context = {
		'login': login_form,
		'error': error,
	}

	context.update(csrf(request))
	return render(request, 'login/index.html', context)

def camera_view(request):
	os.environ['NO_PROXY'] = '127.0.0.1'

	if request.method == 'POST':
		url = request.POST['url']
		
		encode = subf('^data:image/png;base64,', '', url)
		decode = urlsafe_b64decode(encode)
		img = Image.open(io.BytesIO(decode))
		photo = io.BytesIO()
		img.save(photo, 'png')
		photo.seek(0)

		try:
			response = requests.post('http://127.0.0.1:5000/api/recognize', data={'group': 'aluno'}, files={ 'file': ('photo.png', photo, 'image/png') })

			if response.status_code == 200:
				responseJSON = response.json()
				student_codigo = responseJSON['reconhecimento']

				with connection.cursor() as cursor:
					cursor.execute("SELECT id, email, senha_hash FROM aluno WHERE cod_treino=%s", [student_codigo])
					result = cursor.fetchone()

					if result != None:
						data = { 'id': result[0], 'email': result[1], 'senha_hash': result[2] }
						
						login_student = LoginBackend.authenticate(request, data['email'], data['senha_hash'])

						if login_student != None and login_student != False:
							login_student.is_authenticated = True
							login_student.save()
							login(request, login_student, backend='aluno.backend.LoginBackend')
							return redirect('/inicio/')
						else:
							return redirect('login')
					else:
						return redirect('login')
			else:
				return redirect('login')
		except:
			return redirect('login')

	return render(request, 'login/camera.html', {})

@login_required(login_url='login')
def home_view(request):
	return render(request, 'options/index.html', {})

def contact_view(request):
	return render(request, 'login/contact.html', {})

def logout_view (request):
	try:
		logout_email = request.user.email
		logout(request)
		student_session = LoginAluno.objects.get(email=logout_email)
		student_session.delete()
	finally:
		return redirect('login')