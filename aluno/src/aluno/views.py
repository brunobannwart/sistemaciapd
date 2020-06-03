#from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.db import connection
import os, requests, io
from regex import subf
from pybase64 import urlsafe_b64decode
from PIL import Image
from .forms import LoginForm
from .backend import LoginBackend

def login_view(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
	
		if form.is_valid():
			data = form.clean_form()
			login_student = LoginBackend.authenticate(request, data['email'], data['senha_hash'])

			if login_student != None and login_student != False:
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

		response = requests.post('http://127.0.0.1:5000/api/recognize', data={'group': 'aluno'}, files={ 'file': ('photo.png', photo, 'image/png') })

		if response.status_code == 200:
			responseJSON = response.json()
			student_codigo = responseJSON['reconhecimento']

			with connection.cursor() as cursor:
				cursor.execute("SELECT id, email, senha_hash FROM aluno WHERE cod_treino=%s", [student_codigo])
				result = cursor.fetchone()

				if result != None:
					data = {
						'id': result[0],
						'email': result[1],
						'senha_hash': result[2],
					}

					login_student = LoginBackend.authenticate(request, data['email'], data['senha_hash'])

					if login_student != None and login_student != False:
						login(request, login_student, backend='aluno.backend.LoginBackend')
						return redirect('/inicio/')
					else:
						return redirect('login')
				else:
					return redirect('login')
		else:
			return redirect('login')

	return render(request, 'login/camera.html', {})

@login_required(login_url='login')
def home_view(request):
	return render(request, 'options/index.html', {})

def logout_view (request):
	try:
		logout_email = request.user.email
		logout(request)
		with connection.cursor() as cursor:
			cursor.execute("UPDATE aluno SET is_authenticated=%s WHERE email=%s", [0, logout_email])
	finally:
		return redirect('login')